from fastapi import APIRouter, Depends, Request, Query
from app.db.session import DataBasePool, authentication_required
from app.db.models.user import UserRole
from app.helpers.helpers import send_json_response
from app.api.v1.endpoints.functions.search import SearchDB

search_router = APIRouter(prefix="/search", tags=["Search"])
searchdb = SearchDB()

@search_router.get("/shops")
@authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN, UserRole.STATE_CONTRIBUTER])
async def search_shops_endpoint(request: Request, q: str = Query(..., description="Search query for shop name"),db_pool=Depends(DataBasePool.get_pool)):
    return await searchdb.search_shops(request, q, db_pool)

@search_router.get("/items")
@authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN, UserRole.STATE_CONTRIBUTER])
async def search_items_endpoint(request: Request, q: str = Query(..., description="Search query for item"),db_pool=Depends(DataBasePool.get_pool)):
    return await searchdb.search_items(request, q, db_pool)
