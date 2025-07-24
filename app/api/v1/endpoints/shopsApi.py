from fastapi import APIRouter, Depends, Request
from app.api.v1.endpoints.functions.shops import SDB
from app.db.models.user import UserRole
from app.db.schemas.shop import ShopCreate, ShopUpdate
from app.db.session import DataBasePool, authentication_required


shop_router = APIRouter(prefix="/shops", tags=["Shops"])
sdb = SDB() 

@shop_router.post("/create_shop")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def create_shop_endpoint(request: Request, data: ShopCreate, db_pool=Depends(DataBasePool.get_pool)):
    return await sdb.create_shop(request, data, db_pool)

@shop_router.patch("/update_shop")
@authentication_required([UserRole.VENDOR,UserRole.ADMIN])
async def update_shop_endpoint(request: Request, data: ShopUpdate, db_pool=Depends(DataBasePool.get_pool)):
    return await sdb.update_shop(request, data, db_pool)

@shop_router.get("/view_shop")
@authentication_required([UserRole.USER,UserRole.VENDOR,UserRole.ADMIN,UserRole.STATE_CONTRIBUTER])
async def view_shop_endpoint(request: Request, owner_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await sdb.view_shop(request, owner_id, db_pool)

@shop_router.get("/{shop_id}")
@authentication_required([UserRole.USER,UserRole.VENDOR,UserRole.ADMIN,UserRole.STATE_CONTRIBUTER])
async def get_shop_endpoint(request: Request, shop_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await sdb.get_shop(request, shop_id, db_pool)

@shop_router.delete("/{shop_id}")
@authentication_required([UserRole.ADMIN])
async def delete_shop_endpoint(request: Request, shop_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await sdb.delete_shop(request, shop_id, db_pool)

