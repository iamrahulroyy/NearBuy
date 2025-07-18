# from fastapi import APIRouter, Depends, HTTPException
# from sqlmodel import Session, select
# from typing import List
# from app.db.queries import delete_instance, get_all_instances, get_instance, insert_instance, update_instance
# from app.db.session import get_session
# from app.db.models.item import Item
# from app.db.schemas.item import ItemCreate, ItemRead, ItemUpdate

# item_router = APIRouter(prefix="/items", tags=["Items"])


# @item_router.post("/", response_model=ItemRead)
# def create_item(item: ItemCreate, session: Session = Depends(get_session)):
#     if session.exec(select(Item).where(Item.name == item.name)).first():
#         raise HTTPException(status_code=400, detail="Item already exists")
#     return insert_instance(session, Item, item.model_dump())

# @item_router.get("/", response_model=List[ItemRead])
# def get_all_items(session: Session = Depends(get_session)):
#     return get_all_instances(session, Item)

# @item_router.get("/{item_id}", response_model=ItemRead)
# def get_item(item_id: int, session: Session = Depends(get_session)):
#     return get_instance(session, Item, item_id)

# @item_router.put("/{item_id}", response_model=ItemRead)
# def update_item(item_id: int, item_data: ItemUpdate, session: Session = Depends(get_session)):
#     return update_instance(session, Item, item_id, item_data.model_dump(exclude_unset=True))

# @item_router.delete("/{item_id}")
# def delete_item(item_id: int, session: Session = Depends(get_session)):
#     delete_instance(session, Item, item_id)
#     return {"detail": "Item deleted"}
