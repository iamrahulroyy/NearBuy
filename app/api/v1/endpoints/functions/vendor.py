import traceback
from fastapi import Request, status
import typesense
from sqlmodel import Session
from app.db.models.shop import ShopTableEnum
from app.db.models.user import UserTableEnum
from app.db.schemas.shop import VendorShopCreate
from app.db.session import DB
from app.helpers.helpers import send_json_response
from app.helpers.geo import create_point_geometry

db = DB()

class VDB:
    def __init__(self):
        pass

    @staticmethod
    async def create_vendor_shop(request: Request, data: VendorShopCreate, db_pool: Session, ts_client: typesense.Client):
        try:
            current_user_session = request.state.emp
            
            # 1. Automatic Owner Linking
            owner = await db.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"email": current_user_session.email}, all=False)
            if not owner:
                return send_json_response(message="Authenticated user not found.",status=status.HTTP_404_NOT_FOUND,)
            
            owner_id = owner.id

            # 2. Prevent Duplicate Shops Per Vendor
            existing_vendor_shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"owner_id": owner_id}, all=False)
            if existing_vendor_shop:
                return send_json_response(message="You have already created a shop.",status=status.HTTP_409_CONFLICT,)
                

            # 3. Input Validation (Pydantic handles basic validation, here we check for global duplicates)
            exists = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shopName": data.shopName}, all=False)
            if exists:
                return send_json_response(message="A shop with this name already exists.",status=status.HTTP_409_CONFLICT)
            
            geom = create_point_geometry(data.latitude, data.longitude)
            shop_data = data.model_dump(exclude_unset=True)
            shop_data.pop("latitude", None)
            shop_data.pop("longitude", None)
            shop_data["location"] = geom
            shop_data["owner_id"] = owner_id 

            inserted_shop, ok = await db.insert(dbClassNam=ShopTableEnum.SHOP, data=shop_data, db_pool=db_pool)
            
            if not ok or not inserted_shop:
                return send_json_response(message="Could not create shop",status=status.HTTP_500_INTERNAL_SERVER_ERROR,)

            db_pool.commit()
            db_pool.refresh(inserted_shop)

            try:
                shop_document = {
                    "shop_id": str(inserted_shop.shop_id),
                    "owner_id": str(inserted_shop.owner_id),
                    "shopName": inserted_shop.shopName,
                    "fullName": inserted_shop.fullName,
                    "address": inserted_shop.address,
                    "contact": inserted_shop.contact,     
                    "description": inserted_shop.description,  
                    "is_open": inserted_shop.is_open,      
                    "location": [data.latitude, data.longitude],
                }
                ts_client.collections["shops"].documents.create(shop_document)
            except Exception as e:
                print(f"Error indexing shop {inserted_shop.shop_id}: {e}") 

            return send_json_response(message="Shop created successfully",status=status.HTTP_201_CREATED,body={"shop_id": str(inserted_shop.shop_id)},)
            
        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="An error occurred while creating the shop.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)