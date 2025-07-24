from fastapi import APIRouter, Depends, Request
from app.api.v1.endpoints.functions.items import IDB
from app.db.models.user import UserRole
from app.db.schemas.item import ItemCreate, ItemUpdate
from app.db.session import DataBasePool, authentication_required


item_router = APIRouter(prefix="/items", tags=["Items"])
idb = IDB() 

@item_router.post("/add_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def add_item_endpoint(request: Request, data: ItemCreate, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.add_item(request, data, db_pool)

@item_router.get("/get_all_items")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN, UserRole.USER, UserRole.STATE_CONTRIBUTER])
async def get_all_items_endpoint(request: Request, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.get_all_items(request, db_pool)

@item_router.get("/get_item/{itemName}")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN, UserRole.USER, UserRole.STATE_CONTRIBUTER])
async def get_item_endpoint(request: Request, itemName: str, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.get_item(request, itemName, db_pool)

@item_router.patch("/update_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def update_item_endpoint(request: Request, data: ItemUpdate, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.update_item(request, data, db_pool)

@item_router.delete("/delete_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def delete_item_endpoint(request: Request,itemName: str, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.delete_item(request, itemName, db_pool)

