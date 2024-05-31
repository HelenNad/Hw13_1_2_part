from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from sqlalchemy import extract
from src.database.models import Contact, User
from src.schemas import ContactBase


async def search_contacts(name: str, fullname: str, email: str, db: Session, user: User):

    if name:
        contact = db.query(Contact).filter_by(name=name, user=user).all()
        return contact
    if fullname:
        contact = db.query(Contact).filter_by(fullname=fullname, user=user).all()
        return contact
    if email:
        contact = db.query(Contact).filter_by(email=email, user=user).all()
        return contact


async def search_birthday(db: Session, user: User):
    today = datetime.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
            ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)) |
            ((extract('month', Contact.birthday) == end_date.month) & (
                    extract('day', Contact.birthday) <= end_date.day)), user=user
        ).all()

    return contacts


async def get_contacts(offset: int, limit: int, db: Session, user: User):
    return db.query(Contact).filter_by(user=user).offset(offset).limit(limit).all()


async def get_contact(contact_id: int, db: Session, user: User):
    return db.query(Contact).filter(Contact.id == contact_id, user=user).first()


async def create_contact(body: ContactBase, db: Session, user: User):
    contact = Contact(name=body.name,
                      fullname=body.fullname,
                      email=body.email,
                      phone_number=body.phone_number,
                      birthday=body.birthday,
                      description=body.description,
                      user=user)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactBase, db: Session, user: User):
    contact = db.query(Contact).filter(Contact.id == contact_id, user=user).first()
    if contact:
        contact.name = body.name
        contact.fullname = body.fullname
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.description = body.description
    db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session, user: User):
    contact = db.query(Contact).filter(Contact.id == contact_id, user=user).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
