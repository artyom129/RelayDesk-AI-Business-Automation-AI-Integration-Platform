import json
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Workflow, Run, StepRun, DeadLetter, Contact, AuditEvent
from .schemas import WebhookPayload, ManualRunRequest
from .services.workflow_engine import execute_workflow
from .services.demo import ensure_demo_workflow

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RelayDesk AI",
    version="1.0.0",
    description="Business automation and AI integration control center",
)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    db = SessionLocal()
    ensure_demo_workflow(db)
    db.close()

@app.get("/health")
def health():
    return {"status": "ok", "service": "relaydesk-ai"}

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    ensure_demo_workflow(db)
    workflows = list(db.scalars(select(Workflow).order_by(Workflow.id.desc())).all())
    runs = list(db.scalars(select(Run).order_by(Run.id.desc()).limit(12)).all())
    contacts = list(db.scalars(select(Contact).order_by(Contact.updated_at.desc()).limit(10)).all())
    events = list(db.scalars(select(AuditEvent).order_by(AuditEvent.id.desc()).limit(10)).all())
    dlq = list(db.scalars(select(DeadLetter).where(DeadLetter.replayed == False).order_by(DeadLetter.id.desc())).all())

    total_runs = db.scalar(select(func.count()).select_from(Run)) or 0
    success_runs = db.scalar(select(func.count()).select_from(Run).where(Run.status == "success")) or 0
    failed_runs = db.scalar(select(func.count()).select_from(Run).where(Run.status == "failed")) or 0
    contact_count = db.scalar(select(func.count()).select_from(Contact)) or 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "workflows": workflows,
        "runs": runs,
        "contacts": contacts,
        "events": events,
        "dlq": dlq,
        "stats": {
            "runs": total_runs,
            "success": success_runs,
            "failed": failed_runs,
            "contacts": contact_count,
            "workflows": len(workflows),
            "dlq": len(dlq),
        }
    })

@app.post("/webhooks/lead")
def lead_webhook(payload: WebhookPayload, db: Session = Depends(get_db)):
    workflow = ensure_demo_workflow(db)
    run = execute_workflow(db, workflow, payload.model_dump())
    return {
        "run_id": run.id,
        "status": run.status,
        "output": json.loads(run.output_json or "{}"),
        "error": run.error,
    }

@app.post("/workflows/{workflow_id}/run")
def manual_run(workflow_id: int, request: ManualRunRequest, db: Session = Depends(get_db)):
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(404, "Workflow not found")
    run = execute_workflow(db, workflow, request.payload)
    return {"run_id": run.id, "status": run.status, "error": run.error}

@app.post("/demo/run")
def run_demo(db: Session = Depends(get_db)):
    workflow = ensure_demo_workflow(db)
    sample = {
        "name": "Maya Thompson",
        "email": "maya@northstar-ops.com",
        "company": "Northstar Ops",
        "message": "We need urgent CRM and API automation with webhooks and AI qualification.",
        "budget": 7500,
        "source": "website",
    }
    execute_workflow(db, workflow, sample)
    return RedirectResponse("/", status_code=303)

@app.get("/api/workflows")
def api_workflows(db: Session = Depends(get_db)):
    rows = db.scalars(select(Workflow).order_by(Workflow.id)).all()
    return [{
        "id": w.id,
        "name": w.name,
        "trigger_type": w.trigger_type,
        "enabled": w.enabled,
        "definition": json.loads(w.definition_json),
    } for w in rows]

@app.get("/api/runs")
def api_runs(db: Session = Depends(get_db)):
    rows = db.scalars(select(Run).order_by(Run.id.desc()).limit(50)).all()
    return [{
        "id": r.id,
        "workflow_id": r.workflow_id,
        "status": r.status,
        "error": r.error,
        "started_at": r.started_at.isoformat(),
        "finished_at": r.finished_at.isoformat() if r.finished_at else None,
    } for r in rows]

@app.get("/api/runs/{run_id}")
def api_run(run_id: int, db: Session = Depends(get_db)):
    run = db.get(Run, run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    steps = db.scalars(select(StepRun).where(StepRun.run_id == run_id).order_by(StepRun.id)).all()
    return {
        "run": {
            "id": run.id,
            "workflow_id": run.workflow_id,
            "status": run.status,
            "input": json.loads(run.input_json or "{}"),
            "output": json.loads(run.output_json or "{}"),
            "error": run.error,
        },
        "steps": [{
            "step_key": s.step_key,
            "connector": s.connector,
            "status": s.status,
            "attempts": s.attempts,
            "detail": s.detail,
        } for s in steps]
    }

@app.get("/api/contacts")
def api_contacts(db: Session = Depends(get_db)):
    rows = db.scalars(select(Contact).order_by(Contact.updated_at.desc())).all()
    return [{
        "id": c.id,
        "email": c.email,
        "name": c.name,
        "company": c.company,
        "score": c.score,
        "stage": c.stage,
        "source": c.source,
    } for c in rows]
