import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.models import Workflow
from app.services.workflow_engine import execute_workflow

def test_workflow_engine_completes(tmp_path: Path):
    engine = create_engine(f"sqlite:///{tmp_path/'test.db'}")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    wf = Workflow(
        name="test",
        trigger_type="manual",
        definition_json=json.dumps({
            "steps": [
                {"key": "normalize", "connector": "transform", "action": "normalize_lead"},
                {"key": "qualify", "connector": "ai", "action": "qualify"},
                {"key": "crm", "connector": "crm", "action": "upsert"},
            ]
        }),
    )
    db.add(wf)
    db.commit()
    db.refresh(wf)

    run = execute_workflow(db, wf, {
        "email": "lead@example.com",
        "name": "Lead User",
        "company": "ACME",
        "budget": 5000,
        "message": "api automation",
        "source": "test",
    })
    assert run.status == "success"
