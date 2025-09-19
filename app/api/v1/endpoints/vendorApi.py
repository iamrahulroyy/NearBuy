from fastapi import APIRouter, Depends, Request
import typesense
from app.api.v1.endpoints.functions.vendor import VDB
from app.db.models.user import UserRole
from app.db.schemas.shop import VendorShopCreate
from app.db.session import DataBasePool, authentication_required
from typesense_helper.typesense_client import get_typesense_client

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])
vdb = VDB()

@vendor_router.post("/shop", description="vendor ep")
@authentication_required([UserRole.VENDOR])
async def create_shop_for_vendor_endpoint(
    request: Request, 
    data: VendorShopCreate, 
    db_pool=Depends(DataBasePool.get_pool),
    ts_client: typesense.Client = Depends(get_typesense_client)
):
    """
    Authenticated endpoint for a vendor to create their own shop.
    The owner_id is automatically linked from the session cookie.
    """
    return await vdb.create_vendor_shop(request, data, db_pool, ts_client)