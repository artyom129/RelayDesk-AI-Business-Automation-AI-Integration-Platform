import json
from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Workflow, Run, StepRun, DeadLetter
from ..connectors.registry import CONNECTORS
from .audit import audit
from .contact_service import upsert_contact

MAX_ATTEMPTS = 3

def execute_workflow(db: Session, workflow: Workflow, payload: dict) -> Run:
    run = Run(
        workflow_id=workflow.id,
        input_json=json.dumps(payload),
        status="running",
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    audit(db, "workflow_started", "run", run.id, workflow.name)

    try:
        definition = json.loads(workflow.definition_json)
        current = dict(payload)

        for index, step in enumerate(definition.get("steps", []), start=1):
            step_key = step.get("key") or f"step_{index}"
            connector_name = step.get("connector", "transform")
            action = step.get("action", "execute")
            connector = CONNECTORS.get(connector_name)

            if not connector:
                raise RuntimeError(f"Unknown connector: {connector_name}")

            last_detail = ""
            success = False
            for attempt in range(1, MAX_ATTEMPTS + 1):
                result = connector.execute(action, current)
                last_detail = result.detail
                db.add(StepRun(
                    run_id=run.id,
                    step_key=step_key,
                    connector=connector_name,
                    status="success" if result.ok else "retry",
                    attempts=attempt,
                    detail=result.detail,
                ))
                db.commit()

                if result.ok:
                    current = result.data
                    success = True
                    break

            if not success:
                db.add(DeadLetter(
                    run_id=run.id,
                    step_key=step_key,
                    payload_json=json.dumps(current),
                    reason=last_detail,
                ))
                db.commit()
                raise RuntimeError(f"{step_key}: {last_detail}")

        contact = upsert_contact(db, current)
        if contact:
            current["contact_id"] = contact.id

        run.status = "success"
        run.output_json = json.dumps(current)
        run.finished_at = datetime.utcnow()
        db.commit()

        audit(db, "workflow_completed", "run", run.id, f"{workflow.name} completed")
        return run

    except Exception as exc:
        run.status = "failed"
        run.error = str(exc)
        run.finished_at = datetime.utcnow()
        db.commit()
        audit(db, "workflow_failed", "run", run.id, str(exc))
        return run
