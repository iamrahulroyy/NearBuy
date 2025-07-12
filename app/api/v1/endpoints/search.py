from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.db.models.inventory import Inventory
from app.db.models.item import Item
from app.db.models.shop import Shop
from app.db.schemas.inventory import InventoryRead

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/", response_model=List[InventoryRead])
def search_inventory(
    item_name: str = Query(..., min_length=1),
    session: Session = Depends(get_session)
):
    item = session.exec(select(Item).where(Item.name.ilike(f"%{item_name}%"))).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    inventory = session.exec(select(Inventory).where(Inventory.item_id == item.id)).all()
    return inventory
