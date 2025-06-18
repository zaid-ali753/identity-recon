from sqlalchemy.orm import Session
from .models import Contact
from typing import Optional
from datetime import datetime

def consolidate_contacts(email: Optional[str], phone: Optional[str], db: Session):
    matches = db.query(Contact).filter(Contact.deletedAt == None).filter(
        (Contact.email == email) | (Contact.phoneNumber == phone)
    ).all()

    if not matches:
        new_contact = Contact(email=email, phoneNumber=phone, linkPrecedence="primary")
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }

    all_related = []
    for m in matches:
        if m.linkPrecedence == "secondary" and m.linkedId:
            parent = db.query(Contact).filter(Contact.id == m.linkedId).first()
            if parent:
                all_related.append(parent)
        all_related.append(m)

    all_related = list({c.id: c for c in all_related}.values())
    primary = min(all_related, key=lambda c: c.createdAt)
    secondary_contacts = [c for c in all_related if c.id != primary.id]

    emails = {c.email for c in all_related if c.email}
    phones = {c.phoneNumber for c in all_related if c.phoneNumber}

    need_new = (email and email not in emails) or (phone and phone not in phones)
    if need_new:
        new_contact = Contact(email=email, phoneNumber=phone, linkedId=primary.id, linkPrecedence="secondary")
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        secondary_contacts.append(new_contact)

    return {
        "primaryContactId": primary.id,
        "emails": [primary.email] + sorted({c.email for c in secondary_contacts if c.email and c.email != primary.email}),
        "phoneNumbers": [primary.phoneNumber] + sorted({c.phoneNumber for c in secondary_contacts if c.phoneNumber and c.phoneNumber != primary.phoneNumber}),
        "secondaryContactIds": [c.id for c in secondary_contacts]
    }
