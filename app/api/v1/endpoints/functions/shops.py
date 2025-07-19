# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlmodel import Session, select
# from typing import List
# from uuid import UUID
# from app.db.session import get_session
# from app.db.models.shop import Shop
# from app.db.queries import insert_instance, update_instance, delete_instance, get_all_instances, get_instance
# from app.db.schemas.shop import ShopCreate, ShopRead, ShopUpdate

# shop_router = APIRouter(prefix="/shops", tags=["Shops"])


# @shop_router.post("/", response_model=ShopRead)
# def create_shop(shop: ShopCreate, session: Session = Depends(get_session)):
#     return insert_instance(session, Shop, shop.model_dump())

# @shop_router.get("/", response_model=List[ShopRead])
# def get_all_shops(session: Session = Depends(get_session)):
#     return get_all_instances(session, Shop)

# @shop_router.get("/{shop_id}", response_model=ShopRead)
# def get_shop(shop_id: int, session: Session = Depends(get_session)):
#     return get_instance(session, Shop, shop_id)

# @shop_router.put("/{shop_id}", response_model=ShopRead)
# def update_shop(shop_id: int, shop_data: ShopUpdate, session: Session = Depends(get_session)):
#     return update_instance(session, Shop, shop_id, shop_data.model_dump(exclude_unset=True))

# @shop_router.delete("/{shop_id}")
# def delete_shop(shop_id: int, session: Session = Depends(get_session)):
#     delete_instance(session, Shop, shop_id)
#     return {"detail": "Shop deleted"}


from app.db.session import DB


db = DB()

class SDB:
    def __init__(self):
        pass

    @staticmethod
    async def create_shop(request, data, db_pool):
        pass

    @staticmethod
    async def update_shop(request, data, db_pool):
        pass

    @staticmethod
    async def view_shop(request, owner_id, db_pool):
        pass

    @staticmethod
    async def get_shop(request, shop_id, db_pool):
        pass
    
    @staticmethod
    async def delete_shop(request, shop_id, db_pool):
        pass