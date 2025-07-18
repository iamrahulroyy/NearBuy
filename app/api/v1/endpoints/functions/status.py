# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session
# from app.db.session import get_session
# from app.db.models.inventory import Inventory
# from app.db.schemas.inventory import InventoryRead
# from app.db.queries import get_instance

# status_router = APIRouter(prefix="/status", tags=["Status"])



# @status_router.get("/{shop_id}/{item_id}", response_model=InventoryRead)
# def get_inventory_status(shop_id: int, item_id: int, session: Session = Depends(get_session)):
#     return get_instance(session, Inventory, (shop_id, item_id))

