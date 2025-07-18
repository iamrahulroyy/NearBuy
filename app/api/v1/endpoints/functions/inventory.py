# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session, select
# from typing import List
# from app.db.session import get_session
# from app.db.models.inventory import Inventory
# from app.db.models.shop import Shop
# from app.db.models.item import Item
# from app.db.queries import insert_instance, update_instance, delete_instance, get_all_instances
# from app.db.schemas.inventory import InventoryCreate, InventoryRead, InventoryUpdate

# inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


# @inventory_router.post("/", response_model=InventoryRead)
# def add_inventory(entry: InventoryCreate, session: Session = Depends(get_session)):
#     if not session.get(Shop, entry.shop_id) or not session.get(Item, entry.item_id):
#         raise HTTPException(status_code=404, detail="Shop or Item not found")
#     if session.get(Inventory, (entry.shop_id, entry.item_id)):
#         raise HTTPException(status_code=400, detail="Inventory already exists")
#     return insert_instance(session, Inventory, entry.model_dump())

# @inventory_router.get("/", response_model=List[InventoryRead])
# def get_all_inventory(session: Session = Depends(get_session)):
#     return get_all_instances(session, Inventory)

# @inventory_router.put("/", response_model=InventoryRead)
# def update_inventory(entry: InventoryUpdate, session: Session = Depends(get_session)):
#     return update_instance(session, Inventory, (entry.shop_id, entry.item_id), entry.model_dump(exclude_unset=True))

# @inventory_router.delete("/{shop_id}/{item_id}")
# def delete_inventory(shop_id: int, item_id: int, session: Session = Depends(get_session)):
#     delete_instance(session, Inventory, (shop_id, item_id))
#     return {"detail": "Inventory entry deleted"}
