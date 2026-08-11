from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import Contact

def upsert_contact(db: Session, payload: dict) -> Contact | None:
    email = str(payload.get("email", "")).strip().lower()
    if not email:
        return None

    contact = db.scalar(select(Contact).where(Contact.email == email))
    if not contact:
        contact = Contact(email=email)
        db.add(contact)

    contact.name = str(payload.get("name", contact.name or ""))
    contact.company = str(payload.get("company", contact.company or ""))
    contact.score = int(payload.get("ai_score", contact.score or 0))
    contact.stage = "qualified" if contact.score >= 50 else "new"
    contact.source = str(payload.get("source", contact.source or "webhook"))
    contact.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(contact)
    return contact
