import traceback
import uuid
from fastapi import Request,status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.models.item import ItemTableEnum
from app.db.models.shop import ShopTableEnum
from app.db.models.user import UserRole, UserTableEnum
from app.db.schemas.item import ItemCreate, ItemUpdate
from app.db.session import DB
from app.helpers.helpers import get_fastApi_req_data, send_json_response


db = DB()

class IDB:
    def __init__(self):
        pass

    @staticmethod
    async def add_item(request: Request, data: ItemCreate, db_pool: Session):
        import uuid
        try:
            apiData = await get_fastApi_req_data(request)
            if not apiData:
                return send_json_response(message="Invalid request data", status=status.HTTP_403_FORBIDDEN, body={})
            
            current_user = getattr(request.state, "emp", None)
            if not current_user or getattr(current_user, "role", None) not in [UserRole.VENDOR, UserRole.ADMIN]:
                return send_json_response(message="Only vendors can add items.", status=status.HTTP_403_FORBIDDEN, body={})
            
            if len(data.itemName.strip()) == 0:
                return send_json_response(message="Invalid item name", status=status.HTTP_403_FORBIDDEN, body={})
            if data.price <= 0:
                return send_json_response(message="Price must be greater than 0", status=status.HTTP_403_FORBIDDEN, body={})
            
            # --- Shop ID validation ---
            if not getattr(data, "shop_id", None):
                return send_json_response(message="shop_id is required.", status=status.HTTP_400_BAD_REQUEST, body={})
            try:
                shop_id_val = str(uuid.UUID(str(data.shop_id)))
            except Exception:
                return send_json_response(message="Invalid shop_id. Must be UUID.", status=status.HTTP_400_BAD_REQUEST, body={})
            
            # --- Shop must exist and belong to this vendor ---
            shop = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id_val}, all=False)
            if not shop:
                return send_json_response(message="Shop not found.", status=status.HTTP_404_NOT_FOUND, body={})
            
            user = await DB.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"email": current_user.email}, all=False)
            # print(f"DEBUG: Shop Owner ID = {shop.owner_id} | Current User ID = {user.id}")
            if not user or shop.owner_id != user.id:
                return send_json_response(message="You can only add items to your own shop.", status=status.HTTP_403_FORBIDDEN, body={})
            
            existing_item = await DB.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": data.itemName, "shop_id": shop_id_val}, all=False)
            if existing_item:
                return send_json_response(message="Item already exists in this shop", status=status.HTTP_403_FORBIDDEN, body={})
            
            item_data = {
                "itemName": data.itemName.strip(),
                "price": data.price,
                "description": data.description,
                "note": data.note,
                "shop_id": shop_id_val
            }
            inserted_item, ok = await DB.insert(dbClassNam=ItemTableEnum.ITEM, data=item_data, db_pool=db_pool)
            if not ok or not inserted_item:
                return send_json_response(message="Could not create item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            serialized_item = jsonable_encoder(inserted_item)
            serialized_item.pop("id", None)

            db_pool.commit()
            return send_json_response(message="Item added successfully", status=status.HTTP_201_CREATED, body=serialized_item)
        
        except Exception as e:
            print("Exception caught at add_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error adding item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def get_all_items(request: Request, db_pool: Session):
        try:
            items = await db.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, all=True)
            if items is None:
                return send_json_response(message="Error retrieving items", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            serialized_items = [{k: v for k, v in item.items() if k != 'id'} for item in jsonable_encoder(items)] if items else []

            return send_json_response(message="Items retrieved successfully", status=status.HTTP_200_OK, body=serialized_items)
        except Exception as e:
            print("Exception caught at get_all_items: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error retrieving items", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def get_item(request: Request, itemName: str, db_pool: Session):
        try:
            item = await db.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": itemName}, all=False)
            
            if not item:
                return send_json_response(message="Item not found", status=status.HTTP_404_NOT_FOUND, body={})
            
            # serialized_item = jsonable_encoder(item)
            serialized_item = {k: v for k, v in jsonable_encoder(item).items() if k != 'id'}

            return send_json_response(message="Item retrieved successfully", status=status.HTTP_200_OK, body=serialized_item)
            
        except Exception as e:
            print("Exception caught at get_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error retrieving item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_item(request: Request, data: ItemUpdate, db_pool: Session):
        import uuid
        try:
            if not data.itemName or not data.shop_id:
                return send_json_response(message="Both item name and shop ID are required for update.", status=status.HTTP_403_FORBIDDEN, body={})

            try:
                shop_id_val = str(uuid.UUID(str(data.shop_id)))
            except Exception:
                return send_json_response(message="Invalid shop_id format. Must be a valid UUID.", status=status.HTTP_400_BAD_REQUEST, body={})

            existing_item = await DB.get_attr_all(
                dbClassNam=ItemTableEnum.ITEM,
                db_pool=db_pool,
                filters={"itemName": data.itemName, "shop_id": shop_id_val},
                all=False
            )
            if not existing_item:
                return send_json_response(message="Item not found in the specified shop.", status=status.HTTP_404_NOT_FOUND, body={})

            shop = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id_val}, all=False)
            if not shop:
                return send_json_response(message="Shop not found.", status=status.HTTP_404_NOT_FOUND, body={})

            current_user = getattr(request.state, "emp", None)
            if not current_user:
                return send_json_response(message="You do not have permission to update items.", status=status.HTTP_403_FORBIDDEN, body={})

            user = await DB.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"email": current_user.email}, all=False)
            if not user or shop.owner_id != user.id:
                return send_json_response(message="You can only update items in your own shop.", status=status.HTTP_403_FORBIDDEN, body={})

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            update_data.pop("itemName", None)
            update_data.pop("shop_id", None)

            if not update_data:
                return send_json_response(message="No data to update", status=status.HTTP_403_FORBIDDEN, body={})
            if "price" in update_data and update_data["price"] <= 0:
                return send_json_response(message="Price must be greater than 0", status=status.HTTP_403_FORBIDDEN, body={})

            all_same = True
            for key, new_value in update_data.items():
                if hasattr(existing_item, key):
                    current_value = getattr(existing_item, key)
                    if current_value != new_value:
                        all_same = False
                        break

            if all_same:
                serialized_existing = jsonable_encoder(existing_item)
                serialized_existing.pop("id", None)
                return send_json_response(message="No changes detected, item already has the provided values", status=status.HTTP_200_OK, body=serialized_existing)

            identifier = {"itemName": data.itemName, "shop_id": shop_id_val}
            message, success = await DB.update_attr_all(dbClassNam=ItemTableEnum.ITEM, data=update_data, db_pool=db_pool, identifier=identifier)
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            updated_item = await DB.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": data.itemName, "shop_id": shop_id_val}, all=False)
            serialized_item = jsonable_encoder(updated_item)
            serialized_item.pop("id", None)

            return send_json_response(message="Item updated successfully", status=status.HTTP_200_OK, body=serialized_item)
        except Exception as e:
            print("Exception caught at update_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error updating item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def delete_item(request: Request, itemName: str, db_pool: Session):
        try:
            item_to_delete = await DB.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": itemName}, all=False)
            if not item_to_delete:
                return send_json_response(message="Item not found", status=status.HTTP_404_NOT_FOUND, body={})
            
            serialized_item = jsonable_encoder(item_to_delete)
            serialized_item.pop("id", None)
            
            identifier = {"itemName": itemName}
            message, success = await DB.delete_attr(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, identifier=identifier)
            
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            return send_json_response(message="Item deleted successfully", status=status.HTTP_200_OK, body=serialized_item)
            
        except Exception as e:
            print("Exception caught at delete_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error deleting item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


