import json
import traceback
import uuid
from fastapi import Request,status
from fastapi.encoders import jsonable_encoder
import redis
from sqlmodel import Session
import typesense
from app.db.models.item import ItemTableEnum
from app.db.models.shop import ShopTableEnum
from app.db.models.user import UserRole, UserTableEnum
from app.db.schemas.item import ItemCreate, ItemUpdate
from app.db.session import DB
from app.db.table_map import TABLE_CLASS_MAP
from app.helpers.helpers import get_fastApi_req_data, send_json_response


db = DB()

class IDB:
    def __init__(self):
        pass

    @staticmethod
    async def add_item(request: Request, data: ItemCreate, db_pool: Session, ts_client: typesense.Client, redis_client: redis.Redis):
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
            
            if not getattr(data, "shop_id", None):
                return send_json_response(message="shop_id is required.", status=status.HTTP_400_BAD_REQUEST, body={})
            try:
                shop_id_val = str(uuid.UUID(str(data.shop_id)))
            except Exception:
                return send_json_response(message="Invalid shop_id. Must be UUID.", status=status.HTTP_400_BAD_REQUEST, body={})
            
            shop = await DB.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id_val}, all=False)
            if not shop:
                return send_json_response(message="Shop not found.", status=status.HTTP_404_NOT_FOUND, body={})
            
            user = await DB.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"email": current_user.email}, all=False)
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
            
            db_pool.commit()
            db_pool.refresh(inserted_item)

            # --- TYPESENSE INDEXING ---
            try:
                item_document = {
                    'id': str(inserted_item.id),
                    'shop_id': str(inserted_item.shop_id),
                    'itemName': inserted_item.itemName,
                    'price': inserted_item.price,
                    'description': inserted_item.description,
                    'note': inserted_item.note,
                }
                ts_client.collections['items'].documents.create(item_document)
            except Exception as e:
                print(f"Error indexing item {inserted_item.id} in Typesense: {e}")
            # --- END TYPESENSE ---

            # --- CACHE INVALIDATION ---
            # redis_client.delete("all_items_cache")
            for key in redis_client.keys("all_items:*"):
                redis_client.delete(key)

            serialized_item = jsonable_encoder(inserted_item)
            serialized_item.pop("id", None)
            return send_json_response(message="Item added successfully", status=status.HTTP_201_CREATED, body=serialized_item)
        
        except Exception as e:
            db_pool.rollback()
            print("Exception caught at add_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error adding item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

        
        except Exception as e:
            print("Exception caught at add_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error adding item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def get_all_items(request: Request, db_pool: Session, page: int, page_size: int, redis_client: redis.Redis):
        cache_key = f"all_items:page_{page}:size_{page_size}"
        try:
            cached_items = redis_client.get(cache_key)
            if cached_items:
                return send_json_response(message="Items retrieved from cache",status=status.HTTP_200_OK,body=json.loads(cached_items))
            
            offset = (page - 1) * page_size
            model_class = TABLE_CLASS_MAP[ItemTableEnum.ITEM]
            items, total_count = await db.get_attr_all_paginated(dbClassNam=model_class,db_pool=db_pool,offset=offset,limit=page_size)

            if items is None:
                return send_json_response(message="Error retrieving items",status=status.HTTP_500_INTERNAL_SERVER_ERROR,body={})

            serialized_items = [
                {k: v for k, v in item.items() if k != 'id'}
                for item in jsonable_encoder(items)
            ] if items else []

            response_body = {
                "data": serialized_items,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total_count,
                    "pages": (total_count + page_size - 1) // page_size
                }
            }
            redis_client.set(cache_key, json.dumps(response_body), ex=3600)
            
            return send_json_response(message="Items retrieved successfully",status=status.HTTP_200_OK,body=response_body)
        
        except Exception as e:
            print("Exception caught at get_all_items:", str(e))
            traceback.print_exc()
            return send_json_response(message="Error retrieving items",status=status.HTTP_500_INTERNAL_SERVER_ERROR,body={})

    @staticmethod
    async def get_item(request: Request, itemName: str, db_pool: Session, redis_client: redis.Redis):
        cache_key = f"item:{itemName}"
        try:
            cached_item = redis_client.get(cache_key)
            if cached_item:
                return send_json_response(message="Item retrieved from cache",status=status.HTTP_200_OK,body=json.loads(cached_item))
            
            item = await db.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": itemName}, all=False)
            
            if not item:
                return send_json_response(message="Item not found", status=status.HTTP_404_NOT_FOUND, body={})
            
            # serialized_item = jsonable_encoder(item)
            serialized_item = {k: v for k, v in jsonable_encoder(item).items() if k != 'id'}

            redis_client.set(cache_key, json.dumps(serialized_item), ex=3600)

            return send_json_response(message="Item retrieved successfully", status=status.HTTP_200_OK, body=serialized_item)
            
        except Exception as e:
            print("Exception caught at get_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error retrieving item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_item(request: Request, data: ItemUpdate, db_pool: Session, ts_client: typesense.Client, redis_client: redis.Redis):
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

            # ... (rest of your validation logic for shop ownership)

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            update_data.pop("itemName", None)
            update_data.pop("shop_id", None)

            if not update_data:
                return send_json_response(message="No data to update", status=status.HTTP_400_BAD_REQUEST, body={})

            identifier = {"itemName": data.itemName, "shop_id": shop_id_val}
            message, success = await DB.update_attr_all(dbClassNam=ItemTableEnum.ITEM, data=update_data, db_pool=db_pool, identifier=identifier)
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            db_pool.commit()
            # --- CACHE INVALIDATION ---
            redis_client.delete(f"item:{data.itemName}")
            # redis_client.delete("all_items_cache")
            for key in redis_client.keys("all_items:*"):
                redis_client.delete(key)

            # --- TYPESENSE UPDATE ---
            try:
                ts_document_update = {}
                if 'description' in update_data:
                    ts_document_update['description'] = update_data['description']
                # Add other updatable fields here if necessary
                
                if ts_document_update:
                    ts_client.collections['items'].documents[str(existing_item.id)].update(ts_document_update)
            except Exception as e:
                print(f"Error updating item {existing_item.id} in Typesense: {e}")
            # --- END TYPESENSE ---

            updated_item = await DB.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": data.itemName, "shop_id": shop_id_val}, all=False)
            serialized_item = jsonable_encoder(updated_item)
            serialized_item.pop("id", None)

            return send_json_response(message="Item updated successfully", status=status.HTTP_200_OK, body=serialized_item)
        except Exception as e:
            db_pool.rollback()
            print("Exception caught at update_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error updating item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def delete_item(request: Request, itemName: str, db_pool: Session, ts_client: typesense.Client, redis_client: redis.Redis):
        try:
            # Note: Deleting just by name can be ambiguous if multiple shops have the same item name.
            # A better approach would be to require shop_id for deletion.
            # For now, we'll proceed with the current itemName logic.
            item_to_delete = await DB.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"itemName": itemName}, all=False)
            if not item_to_delete:
                return send_json_response(message="Item not found", status=status.HTTP_404_NOT_FOUND, body={})
            
            item_id_to_delete = str(item_to_delete.id)
            serialized_item = jsonable_encoder(item_to_delete)
            serialized_item.pop("id", None)
            
            identifier = {"itemName": itemName}
            message, success = await DB.delete_attr(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, identifier=identifier)
            
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            db_pool.commit()

            # --- CACHE INVALIDATION ---
            redis_client.delete(f"item:{itemName}")
            # redis_client.delete("all_items_cache")
            for key in redis_client.keys("all_items:*"):
                redis_client.delete(key)

            # --- TYPESENSE DELETE ---
            try:
                ts_client.collections['items'].documents[item_id_to_delete].delete()
            except Exception as e:
                print(f"Error deleting item {item_id_to_delete} from Typesense: {e}")
            # --- END TYPESENSE ---
            
            return send_json_response(message="Item deleted successfully", status=status.HTTP_200_OK, body=serialized_item)
            
        except Exception as e:
            db_pool.rollback()
            print("Exception caught at delete_item: ", str(e))
            traceback.print_exc()
            return send_json_response(message="Error deleting item", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


