from fastapi import APIRouter, Depends, Request
from app.api.v1.endpoints.functions.inventory import INDB
from app.db.models.user import UserRole
from app.db.schemas.inventory import InventoryBase, InventoryUpdate
from app.db.session import DataBasePool, authentication_required


inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])

idb = INDB() 

@inventory_router.post("/add")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def add_inventory_endpoint(request: Request, data: InventoryBase, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.add_inventory(request, data, db_pool)

@inventory_router.patch("/update")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def update_inventory_endpoint(request: Request, data: InventoryUpdate, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.update_inventory(request, data, db_pool)

@inventory_router.get("/{inventory_id}")
@authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN])
async def get_inventory_by_id_endpoint(request: Request, inventory_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.get_inventory_by_id(request, inventory_id, db_pool)

@inventory_router.get("/shop/{shop_id}")
@authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN])
async def get_inventory_for_shop_endpoint(request: Request, shop_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.get_inventory_for_shop(request, shop_id, db_pool)

@inventory_router.delete("/{inventory_id}")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def delete_inventory_endpoint(request: Request, inventory_id: str, db_pool=Depends(DataBasePool.get_pool)):
    return await idb.delete_inventory(request, inventory_id, db_pool)
