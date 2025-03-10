from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactBase, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/search_by_elem_body", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_contacts(name: str = None, fullname: str = None, email: str = None,
                          db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.search_contacts(name, fullname, email, db, user)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/search_by_birthday", response_model=list[ContactResponse],
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def search_contacts(db: Session = Depends(get_db), user: User = Depends(auth_service.get_current_user)):

    contacts = await repository_contacts.search_birthday(db, user)

    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/", response_model=list[ContactResponse], dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contacts(offset: int = 0, limit: int = 100, db: Session = Depends(get_db),
                        user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(offset, limit, db, user)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def read_contact(contact_id: int, db: Session = Depends(get_db),
                       user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def create_contact(body: ContactBase, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, db, user)


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def update_contact(body: ContactBase, contact_id: int, db: Session = Depends(get_db),
                         user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse,
               dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def remove_tag(contact_id: int, db: Session = Depends(get_db),
                     user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
