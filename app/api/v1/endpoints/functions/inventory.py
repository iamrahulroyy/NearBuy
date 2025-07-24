import time
import traceback
import uuid
from fastapi import Request,status
from sqlmodel import Session
from app.db.models.inventory import InventoryTableEnum
from app.db.models.item import ItemTableEnum
from app.db.models.shop import ShopTableEnum
from app.db.models.user import UserRole, UserTableEnum
from app.db.schemas.inventory import InventoryBase, InventoryUpdate
from app.db.session import DB
from app.helpers.helpers import extract_model, get_fastApi_req_data, recursive_to_str, send_json_response


db = DB()

class INDB:
    def __init__(self):
        pass

    @staticmethod
    async def add_inventory(request: Request, data: InventoryBase, db_pool: Session):
        try:
            apiData = await get_fastApi_req_data(request)
            if not apiData:
                return send_json_response(message="Invalid request data", status=status.HTTP_403_FORBIDDEN, body={})
            # try:
            #     shop_id_val = str(uuid.UUID(str(data.shop_id)))
            #     item_id_val = str(uuid.UUID(str(data.item_id)))
            # except Exception:
            #     return send_json_response(message="shop_id and item_id must be valid UUIDs.", status=status.HTTP_400_BAD_REQUEST, body={})
            

            shop_id_val = data.shop_id
            item_id_val = data.item_id

            current_user = getattr(request.state, "emp", None)
            if not current_user or getattr(current_user, "role", None) not in [UserRole.VENDOR, UserRole.ADMIN]:
                return send_json_response(message="Only vendors can add inventory.", status=status.HTTP_403_FORBIDDEN, body={})
            
            shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": shop_id_val}, all=False)
            if not shop:
                return send_json_response(message="Shop not found.", status=status.HTTP_404_NOT_FOUND, body={})
            user = await db.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool, filters={"email": current_user.email}, all=False)
            if not user or str(shop.owner_id) != str(user.id):
                return send_json_response(message="You can only add inventory to your own shop.", status=status.HTTP_403_FORBIDDEN, body={})
            
            item = await db.get_attr_all(dbClassNam=ItemTableEnum.ITEM, db_pool=db_pool, filters={"id": item_id_val}, all=False)
            if not item:
                return send_json_response(message="Item not found.", status=status.HTTP_404_NOT_FOUND, body={})
            
            if data.quantity is None or data.quantity < 0:
                return send_json_response(message="Quantity must be zero or positive.", status=status.HTTP_400_BAD_REQUEST, body={})
            if (data.min_quantity is not None and data.max_quantity is not None
            and data.min_quantity > data.max_quantity):
                return send_json_response(message="min_quantity must be less than or equal to max_quantity.", status=status.HTTP_400_BAD_REQUEST, body={})
            if data.expiry_date is not None and data.expiry_date < int(time.time()):
                return send_json_response(message="Expiry date, if provided, must be in the future.", status=status.HTTP_400_BAD_REQUEST, body={})
            
            existing = await db.get_attr_all(
                dbClassNam=InventoryTableEnum.INVENTORY, 
                db_pool=db_pool, 
                filters={"shop_id": shop_id_val, "item_id": item_id_val}, all=False
            )
            if existing:
                return send_json_response(message="Inventory already exists for this item and shop", status=status.HTTP_409_CONFLICT, body={})
            
            inventory_data = data.model_dump(exclude_unset=True, exclude_none=True)
            inventory_data["inventory_id"] = str(uuid.uuid4())
            inventory_data["shop_id"] = shop_id_val
            inventory_data["item_id"] = item_id_val

            inserted, ok = await db.insert(dbClassNam="INVENTORY", data=inventory_data, db_pool=db_pool)
            if not ok or not inserted:
                return send_json_response(message="Could not add inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            
            res = inserted.model_dump(); res.pop("inventory_id", None); res.pop("shop_id", None)

            db_pool.commit()

            return send_json_response(message="Inventory added", status=status.HTTP_201_CREATED, body=res)
        
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error adding inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def update_inventory(request: Request, data: InventoryUpdate, db_pool: Session):
        import uuid, time
        try:
            identifier = {}
            if getattr(data, "inventory_id", None): 
                try:
                    identifier = {"inventory_id": data.inventory_id} 
                except Exception:
                    return send_json_response(message="Invalid inventory_id format (UUID expected).", status=status.HTTP_400_BAD_REQUEST, body={})
                
            elif getattr(data, "shop_id", None) and getattr(data, "item_id", None):   #NOTE currently not validating shop_id and item_id, just inventory_id works even if they are not provided wrong
                try:
                    identifier = {
                        "shop_id": data.shop_id,
                        "item_id": data.item_id,
                    }
                except Exception:
                    return send_json_response(message="shop_id and item_id must be valid UUIDs.", status=status.HTTP_400_BAD_REQUEST, body={})
            else:
                return send_json_response(message="Inventory id or (shop_id & item_id) required", status=status.HTTP_400_BAD_REQUEST, body={})

            old_record = await db.get_attr_all(dbClassNam=InventoryTableEnum.INVENTORY,db_pool=db_pool,filters=identifier,all=False)
            if not old_record:
                return send_json_response(message="Inventory record not found", status=status.HTTP_404_NOT_FOUND, body={})

            shop = await db.get_attr_all(dbClassNam=ShopTableEnum.SHOP, db_pool=db_pool, filters={"shop_id": old_record.shop_id}, all=False)
            current_user = getattr(request.state, "emp", None)
            if not current_user or getattr(current_user, "role", None) not in [UserRole.VENDOR, UserRole.ADMIN]:
                return send_json_response(message="Only vendors can update inventory.", status=status.HTTP_403_FORBIDDEN, body={})
            
            user = await db.get_attr_all(dbClassNam=UserTableEnum.USER, db_pool=db_pool,filters={"email": current_user.email}, all=False)
            if not shop or not user or str(shop.owner_id) != str(user.id):
                return send_json_response(message="You can only update inventory for your own shop.", status=status.HTTP_403_FORBIDDEN, body={})

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            update_data.pop("inventory_id", None)
            update_data.pop("shop_id", None)
            update_data.pop("item_id", None)

            if not update_data:
                return send_json_response(message="No data to update", status=status.HTTP_400_BAD_REQUEST, body=recursive_to_str(old_record.model_dump()))

            if "quantity" in update_data and update_data["quantity"] < 0:
                return send_json_response(message="Quantity must be zero or positive.", status=status.HTTP_400_BAD_REQUEST, body={})
            
            min_q = update_data.get("min_quantity", getattr(old_record, "min_quantity", None))
            max_q = update_data.get("max_quantity", getattr(old_record, "max_quantity", None))

            if min_q is not None and max_q is not None and min_q > max_q:
                return send_json_response(message="min_quantity must be less than or equal to max_quantity.", status=status.HTTP_400_BAD_REQUEST, body={})
            
            if "expiry_date" in update_data:
                if update_data["expiry_date"] < int(time.time()):
                    return send_json_response(message="Expiry date must be in the future.", status=status.HTTP_400_BAD_REQUEST, body={})

            all_same = True
            for key, new_val in update_data.items():
                if hasattr(old_record, key):
                    if getattr(old_record, key) != new_val:
                        all_same = False
                        break
            if all_same:
                serial = recursive_to_str(old_record.model_dump())
                serial.pop("inventory_id", None)
                serial.pop("shop_id", None)
                serial.pop("item_id", None)
                return send_json_response(
                    message="No changes detected, inventory already has provided values",
                    status=status.HTTP_200_OK,
                    body=serial
                )

            message, success = await db.update_attr_all(dbClassNam=InventoryTableEnum.INVENTORY, data=update_data, db_pool=db_pool, identifier=identifier)
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            updated = await db.get_attr_all(dbClassNam=InventoryTableEnum.INVENTORY, db_pool=db_pool, filters=identifier, all=False)
            updated = extract_model(updated)
            serial = recursive_to_str(updated.model_dump())
            serial.pop("inventory_id", None)
            serial.pop("shop_id", None)
            serial.pop("item_id", None)

            return send_json_response(message="Inventory updated", status=status.HTTP_200_OK, body=serial)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error updating inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})


    @staticmethod
    async def get_inventory_by_id(request, inventory_id, db_pool):
        try:
            record = await db.get_attr_all(
                dbClassNam=InventoryTableEnum.INVENTORY, 
                db_pool=db_pool, 
                filters={"inventory_id": inventory_id}, 
                all=False
            )
            record = extract_model(record)
            if not record:
                return send_json_response(message="Not found", status=status.HTTP_404_NOT_FOUND, body={})
            body = recursive_to_str(record.model_dump())
            return send_json_response(message="Inventory found", status=status.HTTP_200_OK, body=body)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error reading inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def get_inventory_for_shop(request, shop_id, db_pool):
        try:
            records = await db.get_attr_all(
                dbClassNam=InventoryTableEnum.INVENTORY, 
                db_pool=db_pool, 
                filters={"shop_id": shop_id}, 
                all=True
            )
            body = [recursive_to_str(extract_model(r).model_dump()) for r in records] if records else []
            return send_json_response(message="Inventories found", status=status.HTTP_200_OK, body=body)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error reading inventories", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body=[])


    @staticmethod
    async def delete_inventory(request, inventory_id, db_pool):
        try:
            record = await db.get_attr_all(
                dbClassNam="INVENTORY", 
                db_pool=db_pool, 
                filters={"inventory_id": inventory_id}, 
                all=False
            )
            record = extract_model(record)
            if not record:
                return send_json_response(message="Not found", status=status.HTTP_404_NOT_FOUND, body={})

            record_dict = recursive_to_str(record.model_dump())

            message, success = await db.delete_attr(
                dbClassNam="INVENTORY", 
                db_pool=db_pool,
                identifier={"inventory_id": inventory_id}
            )
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            return send_json_response(message="Inventory deleted", status=status.HTTP_200_OK, body=record_dict)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error deleting inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})