import json
import traceback
from fastapi import Request,status
from fastapi.encoders import jsonable_encoder
import redis
from sqlmodel import Session
from app.db.models.shop import ShopTableEnum
from app.db.models.user import UserTableEnum
from app.db.schemas.shop import ShopCreate, ShopUpdate
from app.db.session import DB
from app.helpers.helpers import get_fastApi_req_data, recursive_to_str, send_json_response
from app.helpers.geo import create_point_geometry, geometry_to_latlon
import warnings
import typesense


db = DB()

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class SDB:
    def __init__(self):
        pass

    @staticmethod
    async def create_shop(request: Request, data: ShopCreate, db_pool: Session, ts_client: typesense.Client):
        try:
            # if not data.owner_id != request.state.emp:
            #     return send_json_response(
            #         message="You are not authorized to create this shop",
            #         status=status.HTTP_403_FORBIDDEN,
            #     )

            owner = await DB.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"id": data.owner_id}, all=False)
            if not owner:
                return send_json_response(
                    message="Owner ID not found. Please create an account first.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            exists = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP,db_pool=db_pool,filters={"shopName": data.shopName},all=False,)
            if exists:
                return send_json_response(
                    message="Shop already exists", status=status.HTTP_409_CONFLICT
                )
            geom = create_point_geometry(data.latitude, data.longitude)
            shop_data = data.model_dump(
                exclude={"latitude", "longitude"}, exclude_unset=True
            )
            shop_data["location"] = geom

            inserted_shop, ok = await DB.insert(
                dbClassNam=ShopTableEnum.SHOP, data=shop_data, db_pool=db_pool
            )
            if not ok or not inserted_shop:
                return send_json_response(
                    message="Could not create shop",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

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
                    "created_at": inserted_shop.created_at,
                }
                ts_client.collections["shops"].documents.create(shop_document)
            except Exception as e:
                print(f"Error indexing shop {inserted_shop.shop_id}: {e}")

            return send_json_response(message="Shop created successfully", status=status.HTTP_201_CREATED, body={"shop_id": str(inserted_shop.shop_id)},)
        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="Error creating shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_shop(
        request: Request, data: ShopUpdate, db_pool: Session, ts_client: typesense.Client, redis_client: redis.Redis
    ):
        try:
            shop_obj = await DB.get_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                db_pool=db_pool,
                filters={"shop_id": data.shop_id},
                all=False,
            )
            if not shop_obj:
                return send_json_response(
                    message="Shop not found", status=status.HTTP_404_NOT_FOUND
                )

            update_data = data.model_dump(exclude_unset=True)
            ts_update_doc = {}

            if "latitude" in update_data and "longitude" in update_data:
                update_data["location"] = create_point_geometry(
                    data.latitude, data.longitude
                )
                ts_update_doc["location"] = [data.latitude, data.longitude]

            for field in ["shop_id", "latitude", "longitude"]:
                update_data.pop(field, None)
                
            for key, value in update_data.items():
                if key in ["shopName", "fullName", "address", "description"]:
                    ts_update_doc[key] = value

            if not update_data:
                return send_json_response(message="No new data provided.")

            _, success = await DB.update_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                data=update_data,
                db_pool=db_pool,
                identifier={"shop_id": data.shop_id},
            )

            if success:
                db_pool.commit()
                redis_client.delete(f"shop:{data.shop_id}")
                redis_client.delete(f"shops_by_owner:{shop_obj.owner_id}")
                if ts_update_doc:
                    try:
                        ts_client.collections["shops"].documents[str(data.shop_id)].update(ts_update_doc)
                    except Exception as e:
                        print(f"Error updating shop in Typesense {data.shop_id}: {e}")
                return send_json_response(message="Shop updated successfully.")
            else:
                return send_json_response(
                    message="Shop update failed",
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(
                message="An error occurred",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    async def view_shop(request, owner_id, db_pool,redis_client: redis.Redis):
        cache_key = f"shops_by_owner:{owner_id}"
        try:
            cached_shops = redis_client.get(cache_key)
            if cached_shops:
                return send_json_response(
                    message="Shops retrieved from cache",
                    status=status.HTTP_200_OK,
                    body=json.loads(cached_shops)
                )
            if not owner_id:
                return send_json_response(message="owner_id is required.", status=status.HTTP_400_BAD_REQUEST, body=[])
            shops = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP,db_pool=db_pool,filters={"owner_id": owner_id},all=True)
            if not shops:
                return send_json_response(message="No shop found", status=status.HTTP_404_NOT_FOUND, body=[])
            result = []
            for shop in shops:
                # shop_dict = shop.model_dump(exclude={"location", "shop_id", "owner_id"})
                shop_dict = jsonable_encoder(shop)
                if shop.location:
                    shop_dict.update(geometry_to_latlon(shop.location))
                shop_dict.pop("location", None)
                result.append(shop_dict)

            result_str = recursive_to_str(result)
            redis_client.set(cache_key, json.dumps(result_str), ex=3600) # Cache for 1 hour
            
            return send_json_response(message="Shops retrieved from DATABASE", status=status.HTTP_200_OK, body=result)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error retrieving shops", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body=[])

    @staticmethod
    async def get_shop(request: Request, shop_id: str, db_pool: Session,redis_client: redis.Redis):
        cache_key = f"shop:{shop_id}"
        try:
            cached_shop = redis_client.get(cache_key)
            if cached_shop:
                return send_json_response(
                    message="Shop retrieved from cache",
                    status=status.HTTP_200_OK,
                    body=json.loads(cached_shop)
                )

            # shop_id may be UUID (not int)
            shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id}, all=False)
            if not shop:
                return send_json_response(message="Shop not found",status=status.HTTP_404_NOT_FOUND,body={})

            shop_dict = jsonable_encoder(shop)
            latlon = geometry_to_latlon(shop.location)
            shop_dict.update(latlon)
            shop_dict.pop("location", None)
            shop_dict.pop("shop_id", None)
            shop_dict.pop("owner_id", None)

            shop_dict = recursive_to_str(shop_dict)
            redis_client.set(cache_key, json.dumps(shop_dict), ex=3600)


            return send_json_response(message="Shop retrieved",status=status.HTTP_200_OK,body=shop_dict)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(
                message="Error retrieving shop",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body={}
            )


    @staticmethod
    async def delete_shop(request: Request, shop_id: str, db_pool: Session, ts_client: typesense.Client, redis_client: redis.Redis):
        try:
            shop = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id}, all=False)
            if not shop:
                return send_json_response(message="Shop not found", status=status.HTTP_404_NOT_FOUND)
            
            _, success = await DB.delete_attr(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, identifier={"shop_id": shop_id})

            if success:
                db_pool.commit()
                redis_client.delete(f"shop:{shop_id}")
                redis_client.delete(f"shops_by_owner:{shop.owner_id}")
                try:
                    ts_client.collections['shops'].documents[str(shop_id)].delete()
                except Exception as e:
                    print(f"Error deleting shop from Typesense {shop_id}: {e}")
                return send_json_response(message="Shop deleted successfully.")
            else:
                 return send_json_response(message="Failed to delete shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="An error occurred", status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    