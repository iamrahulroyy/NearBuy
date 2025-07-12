from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.db.models.inventory import Inventory
from app.db.models.shop import Shop
from app.db.models.item import Item
from app.db.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate

inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.post("/", response_model=InventoryRead)
def add_inventory(entry: InventoryCreate, session: Session = Depends(get_session)):
    shop = session.get(Shop, entry.shop_id)
    item = session.get(Item, entry.item_id)
    if not shop or not item:
        raise HTTPException(status_code=404, detail="Shop or Item not found")

    existing = session.get(Inventory, (entry.shop_id, entry.item_id))
    if existing:
        raise HTTPException(status_code=400, detail="Inventory already exists")

    inventory = Inventory.model_validate(entry)
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


@inventory_router.get("/", response_model=List[InventoryRead])
def get_all_inventory(session: Session = Depends(get_session)):
    return session.exec(select(Inventory)).all()


@inventory_router.put("/", response_model=InventoryRead)
def update_inventory(entry: InventoryUpdate, session: Session = Depends(get_session)):
    inventory = session.get(Inventory, (entry.shop_id, entry.item_id))
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    inventory.quantity = entry.quantity
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory


@inventory_router.delete("/{shop_id}/{item_id}")
def delete_inventory(shop_id: int, item_id: int, session: Session = Depends(get_session)):
    inventory = session.get(Inventory, (shop_id, item_id))
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    session.delete(inventory)
    session.commit()
    return {"detail": "Inventory entry deleted"}
