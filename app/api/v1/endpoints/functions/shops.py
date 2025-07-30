import traceback
from fastapi import Request,status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.models.shop import ShopTableEnum
from app.db.schemas.shop import ShopCreate, ShopUpdate
from app.db.session import DB
from app.helpers.helpers import get_fastApi_req_data, recursive_to_str, send_json_response
from app.helpers.geo import create_point_geometry, geometry_to_latlon
import warnings
import typesense
from app.core.typesense_client import get_typesense_client


db = DB()

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class SDB:
    def __init__(self):
        pass

    @staticmethod
    async def create_shop(request: Request, data: ShopCreate, db_pool: Session, ts_client: typesense.Client):
        try:
            apiData = await get_fastApi_req_data(request)
            exists = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shopName": data.shopName}, all=False)
            if exists:
                return send_json_response(message="Shop already exists", status=status.HTTP_403_FORBIDDEN, body={})
            
            # --- OWNER_ID CHECK ---
            if not getattr(data, "owner_id", None):
                return send_json_response(message="Missing owner_id! Unable to create shop.", status=status.HTTP_400_BAD_REQUEST, body={})
            owner_exists = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"owner_id": data.owner_id}, all=False)
            if not owner_exists:
                return send_json_response(message="The provided owner_id does not exist. Please register first.", status=status.HTTP_400_BAD_REQUEST, body={})

            geom = create_point_geometry(data.latitude, data.longitude)
            shop_data = data.model_dump(exclude_unset=True, exclude_none=True)
            shop_data["location"] = geom
            shop_data.pop("latitude", None)
            shop_data.pop("longitude", None)

            inserted_shop, ok = await DB.insert(dbClassNam=ShopTableEnum.SHOP, data=shop_data, db_pool=db_pool)
            if not ok or not inserted_shop:
                return send_json_response(message="Could not create shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            db_pool.commit()

            # --- TYPESENSE INDEXING ---
            try:
                shop_document = {
                    'id': str(inserted_shop.shop_id),
                    'name': inserted_shop.shopName,
                    'address': inserted_shop.address,
                    'location': [data.latitude, data.longitude]
                }
                ts_client.collections['shops'].documents.create(shop_document)
            except Exception as e:
                print(f"Error indexing shop {inserted_shop.shop_id} in Typesense: {e}")
            # --- END TYPESENSE ---

            shop_dict = inserted_shop.model_dump(exclude={"location", "shop_id"})
            latlon = geometry_to_latlon(inserted_shop.location)
            shop_dict.update(latlon)

            shop_dict = recursive_to_str(shop_dict)
            shop_dict.pop("shop_id", None)
            shop_dict.pop("owner_id", None)

            return send_json_response(message="Shop created successfully", status=status.HTTP_201_CREATED, body=shop_dict)
        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="Error creating shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_shop(request: Request, data: ShopUpdate, db_pool: Session, ts_client: typesense.Client):
        try:
            update_data = data.model_dump(exclude_unset=True)
            if not data.shop_id:
                return send_json_response(message="Shop ID is required to update a shop.", status=status.HTTP_400_BAD_REQUEST)

            shop_obj = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": data.shop_id}, all=False)
            if not shop_obj:
                return send_json_response(message="Shop not found.", status=status.HTTP_404_NOT_FOUND)

            lat, lon = data.latitude, data.longitude
            if "latitude" in update_data and "longitude" in update_data:
                update_data["location"] = create_point_geometry(lat, lon)

            for field in ["shop_id", "owner_id", "latitude", "longitude"]:
                update_data.pop(field, None)

            if not update_data:
                return send_json_response(message="No new data provided to update.", status=status.HTTP_200_OK)

            message, success = await DB.update_attr_all(
                dbClassNam=ShopTableEnum.SHOP, 
                data=update_data, 
                db_pool=db_pool, 
                identifier={"shop_id": data.shop_id}
            )
            if not success:
                return send_json_response(message=message, status=status.HTTP_400_BAD_REQUEST)

            db_pool.commit()

            # --- TYPESENSE UPDATE ---
            try:
                ts_document = {}
                if 'shopName' in update_data:
                    ts_document['name'] = update_data['shopName']
                if 'address' in update_data:
                    ts_document['address'] = update_data['address']
                if 'location' in update_data:
                    ts_document['location'] = [lat, lon]
                
                if ts_document:
                    ts_client.collections['shops'].documents[str(data.shop_id)].update(ts_document)
            except Exception as e:
                print(f"Error updating shop {data.shop_id} in Typesense: {e}")
            # --- END TYPESENSE ---

            updated_shop = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": data.shop_id}, all=False)
            shop_dict = updated_shop.model_dump(exclude={"location"}) if updated_shop else {}
            if updated_shop and updated_shop.location:
                shop_dict.update(geometry_to_latlon(updated_shop.location))
                shop_dict = recursive_to_str(shop_dict)

            return send_json_response(message="Shop updated successfully", status=status.HTTP_200_OK, body=shop_dict)
        except Exception as e:
            if db_pool:
                db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="An error occurred while updating the shop.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def view_shop(request, owner_id, db_pool):
        try:
            if not owner_id:
                return send_json_response(message="owner_id is required.", status=status.HTTP_400_BAD_REQUEST, body=[])
            shops = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP,db_pool=db_pool,filters={"owner_id": owner_id},all=True)
            if not shops:
                return send_json_response(message="No shop found", status=status.HTTP_404_NOT_FOUND, body=[])
            result = []
            for shop in shops:
                shop_dict = shop.model_dump(exclude={"location", "shop_id", "owner_id"})
                if shop.location:
                    shop_dict.update(geometry_to_latlon(shop.location))
                result.append(shop_dict)
            return send_json_response(message="Shops retrieved", status=status.HTTP_200_OK, body=result)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error retrieving shops", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body=[])

    @staticmethod
    async def get_shop(request: Request, shop_id: str, db_pool: Session):
        try:
            # shop_id may be UUID (not int)
            shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id}, all=False)
            if not shop:
                return send_json_response(message="Shop not found",status=status.HTTP_404_NOT_FOUND,body={})

            shop_dict = shop.model_dump()
            latlon = geometry_to_latlon(shop.location)
            shop_dict.update(latlon)
            shop_dict.pop("location", None)
            shop_dict.pop("shop_id", None)
            shop_dict.pop("owner_id", None)

            shop_dict = recursive_to_str(shop_dict)

            return send_json_response(message="Shop retrieved",status=status.HTTP_200_OK,body=shop_dict)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(
                message="Error retrieving shop",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body={}
            )


    @staticmethod
    async def delete_shop(request: Request, shop_id: str, db_pool: Session, ts_client: typesense.Client):
        try:
            shop_id_val = str(shop_id)
            shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id_val}, all=False)
            if not shop:
                return send_json_response(message="Shop not found", status=status.HTTP_404_NOT_FOUND, body={})
            
            shop_dict = shop.model_dump(exclude={"location"})
            if shop.location:
                shop_dict.update(geometry_to_latlon(shop.location))
            shop_dict.pop("shop_id", None)
            shop_dict = recursive_to_str(shop_dict)

            message, success = await DB.delete_attr(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, identifier={"shop_id": shop_id_val})
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            db_pool.commit()

            # --- TYPESENSE DELETE ---
            try:
                ts_client.collections['shops'].documents[shop_id_val].delete()
            except Exception as e:
                 print(f"Error deleting shop {shop_id_val} from Typesense: {e}")
            # --- END TYPESENSE ---

            return send_json_response(message="Shop deleted successfully", status=status.HTTP_200_OK, body=shop_dict)
        except Exception as e:
            db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="Error deleting shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})




    