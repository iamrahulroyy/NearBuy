import traceback
import uuid
from fastapi import Request,status
from sqlmodel import Session
from app.db.models.inventory import InventoryTableEnum
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
            
            inventory_data = data.model_dump(exclude_unset=True, exclude_none=True)
            inventory_data["inventory_id"] = str(uuid.uuid4())
            existing = await db.get_attr_all(
                dbClassNam=InventoryTableEnum.INVENTORY, 
                db_pool=db_pool, 
                filters={
                    "shop_id": inventory_data.get("shop_id"),
                    "item_id": inventory_data.get("item_id")
                }, 
                all=False
            )
            if existing:
                return send_json_response(message="Inventory already exists for this item and shop", status=status.HTTP_409_CONFLICT, body={})

            inserted, ok = await db.insert(dbClassNam="INVENTORY", data=inventory_data, db_pool=db_pool)
            if not ok or not inserted:
                return send_json_response(message="Could not add inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            res = inserted.model_dump()
            res.pop("inventory_id", None)
            res.pop("shop_id", None)

            db_pool.commit()
            return send_json_response(message="Inventory added", status=status.HTTP_201_CREATED, body=res)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error adding inventory", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

    @staticmethod
    async def update_inventory(request: Request, data: InventoryUpdate, db_pool: Session):
        try:
            identifier = {}
            if getattr(data, "inventory_id", None):
                identifier = {"inventory_id": data.inventory_id}
            elif getattr(data, "shop_id", None) and getattr(data, "item_id", None):
                identifier = {"shop_id": data.shop_id, "item_id": data.item_id}
            else:
                return send_json_response(message="Inventory id or (shop_id & item_id) required", status=status.HTTP_400_BAD_REQUEST, body={})

            old = await db.get_attr_all(
                dbClassNam=InventoryTableEnum.INVENTORY, 
                db_pool=db_pool, 
                filters=identifier, 
                all=False
            )
            if not old:
                return send_json_response(message="Inventory record not found", status=status.HTTP_404_NOT_FOUND, body={})

            update_data = data.model_dump(exclude_unset=True, exclude_none=True)
            update_data.pop("inventory_id", None)
            update_data.pop("shop_id", None)
            update_data.pop("item_id", None)
            if not update_data:
                return send_json_response(message="No data to update", status=status.HTTP_400_BAD_REQUEST, body=recursive_to_str(old.model_dump()))

            message, success = await db.update_attr_all(dbClassNam=InventoryTableEnum.INVENTORY,data=update_data,db_pool=db_pool,identifier=identifier)
            if not success:
                return send_json_response(message=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

            updated = await db.get_attr_all(dbClassNam=InventoryTableEnum.INVENTORY, db_pool=db_pool, filters=identifier, all=False)

            updated = extract_model(updated)
            serial = recursive_to_str(updated.model_dump())
            serial.pop("inventory_id", None)
            serial.pop("shop_id", None)
            serial.pop("item_id", None)


            return send_json_response(message="Inventory updated",status=status.HTTP_200_OK,body=serial)
        
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