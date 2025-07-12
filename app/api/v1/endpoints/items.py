from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.db.models.item import Item
from app.db.schemas.item import ItemCreate, ItemRead, ItemUpdate

item_router = APIRouter(prefix="/items", tags=["Items"])


@item_router.post("/", response_model=ItemRead)
def create_item(item: ItemCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(Item).where(Item.name == item.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Item already exists")
    db_item = Item.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@item_router.get("/", response_model=List[ItemRead])
def get_all_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()


@item_router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@item_router.put("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.sqlmodel_update(item_data.model_dump(exclude_unset=True))
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@item_router.delete("/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"detail": "Item deleted"}
