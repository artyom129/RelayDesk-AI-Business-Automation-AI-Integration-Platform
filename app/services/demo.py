import json
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Workflow

DEMO_WORKFLOW = {
    "steps": [
        {"key": "normalize", "connector": "transform", "action": "normalize_lead"},
        {"key": "qualify", "connector": "ai", "action": "qualify"},
        {"key": "crm_upsert", "connector": "crm", "action": "upsert_contact"},
        {"key": "sheet_log", "connector": "sheets", "action": "append"},
        {"key": "welcome_email", "connector": "email", "action": "lead_welcome"},
        {"key": "admin_alert", "connector": "chatbot", "action": "qualified_lead_alert"},
    ]
}

def ensure_demo_workflow(db: Session) -> Workflow:
    workflow = db.scalar(select(Workflow).where(Workflow.name == "AI Lead Intake & CRM Sync"))
    if workflow:
        return workflow
    workflow = Workflow(
        name="AI Lead Intake & CRM Sync",
        trigger_type="webhook",
        enabled=True,
        definition_json=json.dumps(DEMO_WORKFLOW),
    )
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow
