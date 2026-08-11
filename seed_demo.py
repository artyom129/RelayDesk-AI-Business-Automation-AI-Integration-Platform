from app.db import Base, engine, SessionLocal
from app.models import Run, StepRun, DeadLetter, Contact, AuditEvent, Workflow
from app.services.demo import ensure_demo_workflow
from app.services.workflow_engine import execute_workflow

Base.metadata.create_all(bind=engine)
db = SessionLocal()

for model in (StepRun, DeadLetter, Run, Contact, AuditEvent, Workflow):
    db.query(model).delete()
db.commit()

workflow = ensure_demo_workflow(db)

samples = [
    {
        "name": "Maya Thompson",
        "email": "maya@northstar-ops.com",
        "company": "Northstar Ops",
        "message": "Urgent CRM API integration and automation project.",
        "budget": 7500,
        "source": "website",
    },
    {
        "name": "Leo Martin",
        "email": "leo@brightlane.co",
        "company": "BrightLane",
        "message": "Need a webhook workflow and spreadsheet sync.",
        "budget": 2800,
        "source": "linkedin",
    },
    {
        "name": "Sara Kim",
        "email": "sara@localstudio.io",
        "company": "Local Studio",
        "message": "Looking for a small email automation.",
        "budget": 650,
        "source": "referral",
    },
]

for sample in samples:
    execute_workflow(db, workflow, sample)

db.close()
print("RelayDesk AI demo data created.")
