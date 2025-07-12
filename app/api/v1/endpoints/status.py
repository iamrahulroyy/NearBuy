from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.db.models.inventory import Inventory
from app.db.schemas.inventory import InventoryRead

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/{shop_id}/{item_id}", response_model=InventoryRead)
def get_inventory_status(
    shop_id: int,
    item_id: int,
    session: Session = Depends(get_session)
):
    inventory = session.get(Inventory, (shop_id, item_id))
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory entry not found")
    return inventory
