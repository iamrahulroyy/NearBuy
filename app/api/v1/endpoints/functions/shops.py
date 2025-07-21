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


db = DB()

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class SDB:
    def __init__(self):
        pass

    @staticmethod
    async def create_shop(request: Request, data: ShopCreate, db_pool: Session):
        try:
            apiData = await get_fastApi_req_data(request)
            exists = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shopName": data.shopName}, all=False)
            if exists:
                return send_json_response(message="Shop already exists", status=status.HTTP_403_FORBIDDEN, body={})

            geom = create_point_geometry(data.latitude, data.longitude)
            shop_data = data.model_dump(exclude_unset=True, exclude_none=True)
            shop_data["location"] = geom
            shop_data.pop("latitude", None)
            shop_data.pop("longitude", None)

            inserted_shop, ok = await DB.insert(dbClassNam=ShopTableEnum.SHOP, data=shop_data, db_pool=db_pool)
            if not ok or not inserted_shop:
                return send_json_response(message="Could not create shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            shop_dict = inserted_shop.model_dump(exclude={"location", "shop_id"})
            latlon = geometry_to_latlon(inserted_shop.location)
            shop_dict.update(latlon)

            shop_dict = recursive_to_str(shop_dict)
            shop_dict.pop("shop_id", None)
            shop_dict.pop("owner_id", None)


            db_pool.commit()

            return send_json_response(message="Shop created successfully", status=status.HTTP_201_CREATED, body=shop_dict)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error creating shop", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_shop(request: Request, data: ShopUpdate, db_pool: Session):
        try:
            identifier = None
            if getattr(data, "shop_id", None):
                identifier = {"shop_id": data.shop_id}
            elif getattr(data, "shopName", None):
                identifier = {"shopName": data.shopName}
            else:
                return send_json_response(
                    message="Shop ID or Shop Name required for update",
                    status=status.HTTP_403_FORBIDDEN,
                    body={}
                )

            old_shop = await DB.get_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                db_pool=db_pool,
                filters=identifier,
                all=False
            )
            if not old_shop:
                return send_json_response(
                    message="Shop not found",
                    status=status.HTTP_404_NOT_FOUND,
                    body={}
                )
            
            # Security: Allow update only if current user owns the shop (#TODO)
            # user = request.state.user if hasattr(request.state, "user") else None  
            # if user and str(old_shop.owner_id) != str(user.id):
            #     return send_json_response(message="Forbidden: You do not own this shop", status=status.HTTP_403_FORBIDDEN, body={})

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            update_data.pop("shop_id", None)
            update_data.pop("shopName", None)
            if "latitude" in update_data or "longitude" in update_data:
                lat = update_data.pop("latitude", None)
                lon = update_data.pop("longitude", None)
                if lat is not None and lon is not None:
                    geom = create_point_geometry(lat, lon)
                    update_data["location"] = geom

            if not update_data:
                shop_dict = old_shop.model_dump(exclude={"location", "shop_id"})
                latlon = geometry_to_latlon(old_shop.location)
                shop_dict.update(latlon)
                shop_dict.pop("owner_id", None)
                return send_json_response(
                    message="No data to update",
                    status=status.HTTP_403_FORBIDDEN,
                    body=shop_dict
                )

            all_same = all(
                getattr(old_shop, k, None) == v
                for k, v in update_data.items()
            )
            if all_same:
                shop_dict = old_shop.model_dump(exclude={"location", "shop_id"})
                latlon = geometry_to_latlon(old_shop.location)
                shop_dict.update(latlon)
                shop_dict.pop("owner_id", None)
                return send_json_response(
                    message="No changes detected",
                    status=status.HTTP_200_OK,
                    body=shop_dict
                )

            message, success = await DB.update_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                data=update_data,
                db_pool=db_pool,
                identifier=identifier
            )
            if not success:
                return send_json_response(
                    message=message,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    body={}
                )

            shop = await DB.get_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                db_pool=db_pool,
                filters=identifier,
                all=False
            )
            shop_dict = shop.model_dump(exclude={"location", "shop_id"})
            latlon = geometry_to_latlon(shop.location)
            shop_dict.update(latlon)
            shop_dict.pop("owner_id", None)
            return send_json_response(
                message="Shop updated successfully",
                status=status.HTTP_200_OK,
                body=shop_dict
            )
        except Exception as e:
            traceback.print_exc()
            return send_json_response(
                message="Error updating shop",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body={}
            )

    @staticmethod
    async def view_shop(request, owner_id, db_pool):
        try:
            shops = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"owner_id": owner_id}, all=True)
            if not shops:
                return send_json_response(message="No shop found", status=status.HTTP_404_NOT_FOUND, body=[])
            result = []
            for shop in shops:
                shop_dict = shop.model_dump()
                latlon = geometry_to_latlon(shop.location)
                shop_dict.update(latlon)
                shop_dict.pop("location", None)
                shop_dict.pop("shop_id", None)
                shop_dict.pop("owner_id", None)
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
    async def delete_shop(request: Request, shop_id: str, db_pool):
        try:
            shop = await db.get_attr_all(
                dbClassNam=ShopTableEnum.SHOP,
                db_pool=db_pool,
                filters={"shop_id": shop_id},
                all=False
            )
            if not shop:
                return send_json_response(
                    message="Shop not found",
                    status=status.HTTP_404_NOT_FOUND,
                    body={}
                )
            shop_dict = shop.model_dump()
            if "location" in shop_dict:
                latlon = geometry_to_latlon(shop.location)
                shop_dict.update(latlon)
                shop_dict.pop("location", None)
            shop_dict.pop("shop_id", None)
            from app.helpers.helpers import recursive_to_str
            shop_dict = recursive_to_str(shop_dict)

            message, success = await DB.delete_attr(
                dbClassNam=ShopTableEnum.SHOP,
                db_pool=db_pool,
                identifier={"shop_id": shop_id}
            )

            if not success:
                return send_json_response(
                    message=message,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    body={}
                )

            return send_json_response(
                message="Shop deleted successfully",
                status=status.HTTP_200_OK,
                body=shop_dict
            )
        except Exception as e:
            traceback.print_exc()
            return send_json_response(
                message="Error deleting shop",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body={}
            )



    