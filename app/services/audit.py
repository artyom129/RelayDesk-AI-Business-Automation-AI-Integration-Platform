from sqlalchemy.orm import Session
from ..models import AuditEvent

def audit(db: Session, event_type: str, entity: str = "", entity_id: str = "", detail: str = ""):
    db.add(AuditEvent(
        event_type=event_type,
        entity=entity,
        entity_id=str(entity_id),
        detail=detail,
    ))
    db.commit()
