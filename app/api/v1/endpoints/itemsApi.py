from fastapi import APIRouter, Depends, Query, Request
import redis
import typesense
from RDB.redis_client import get_redis_client
from app.api.v1.endpoints.functions.items import IDB
from app.db.models.user import UserRole
from app.db.schemas.item import ItemCreate, ItemUpdate
from app.db.session import DataBasePool, authentication_required
from typesense_helper.typesense_client import get_typesense_client


item_router = APIRouter(prefix="/items", tags=["Items"])
idb = IDB() 

@item_router.post("/add_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def add_item_endpoint(request: Request, data: ItemCreate, db_pool=Depends(DataBasePool.get_pool),ts_client: typesense.Client = Depends(get_typesense_client), redis_client: redis.Redis = Depends(get_redis_client)):
    return await idb.add_item(request, data, db_pool,ts_client, redis_client)

@item_router.get("/get_all_items")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN, UserRole.USER, UserRole.STATE_CONTRIBUTER])
async def get_all_items_endpoint(request: Request,db_pool=Depends(DataBasePool.get_pool),page: int = Query(1, gt=0),page_size: int = Query(20, gt=0, le=100), redis_client: redis.Redis = Depends(get_redis_client)):
    return await idb.get_all_items(request, db_pool, page, page_size, redis_client)

@item_router.get("/get_item/{itemName}")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN, UserRole.USER, UserRole.STATE_CONTRIBUTER])
async def get_item_endpoint(request: Request, itemName: str, db_pool=Depends(DataBasePool.get_pool), redis_client: redis.Redis = Depends(get_redis_client)):
    return await idb.get_item(request, itemName, db_pool, redis_client)

@item_router.patch("/update_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def update_item_endpoint(request: Request, data: ItemUpdate, db_pool=Depends(DataBasePool.get_pool),ts_client: typesense.Client = Depends(get_typesense_client), redis_client: redis.Redis = Depends(get_redis_client)):
    return await idb.update_item(request, data, db_pool,ts_client, redis_client)

@item_router.delete("/delete_item")
@authentication_required([UserRole.VENDOR, UserRole.ADMIN])
async def delete_item_endpoint(request: Request,itemName: str, db_pool=Depends(DataBasePool.get_pool),ts_client: typesense.Client = Depends(get_typesense_client), redis_client: redis.Redis = Depends(get_redis_client)):
    return await idb.delete_item(request, itemName, db_pool,ts_client, redis_client)

