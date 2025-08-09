import traceback
from fastapi import APIRouter, Depends, HTTPException, Request, Query
import typesense
from app.core.limiter import limiter  
from app.api.v1.endpoints.functions.search import SearchDB
from typesense_helper.typesense_client import get_typesense_client

search_router = APIRouter(prefix="/search", tags=["Search"])
searchdb = SearchDB()

# @search_router.get("/shops", description="Search for shops by name {public}")
# # @authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN, UserRole.STATE_CONTRIBUTER])
# async def search_shops_endpoint(request: Request, q: str = Query(..., description="Search query for shop name"),db_pool=Depends(DataBasePool.get_pool)):
#     return await searchdb.search_shops(request, q, db_pool)

# @search_router.get("/items", description="Search for items by name or description {public}")
# # @authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN, UserRole.STATE_CONTRIBUTER])
# async def search_items_endpoint(request: Request, q: str = Query(..., description="Search query for item"),db_pool=Depends(DataBasePool.get_pool)):
#     return await searchdb.search_items(request, q, db_pool)

@search_router.get("/nearby", description="Search for items available in shops near a specific location.")
@limiter.limit("30/minute")
def search_nearby_endpoint(
    request: Request,
    q: str = Query(..., description="The item you are searching for (e.g., 'coffee', 'batteries').", min_length=1),
    lat: float = Query(..., description="Your current latitude.", ge=-90, le=90),
    lon: float = Query(..., description="Your current longitude.", ge=-180, le=180),
    radius_km: int = Query(5, description="The search radius in kilometers.", ge=1, le=50),
    ts_client: typesense.Client = Depends(get_typesense_client)
):
    try:
        results = searchdb.search_nearby_items(q=q, lat=lat, lon=lon, radius_km=radius_km, ts_client=ts_client)
        return results
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        print(f"An unexpected error occurred in the search endpoint: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")
