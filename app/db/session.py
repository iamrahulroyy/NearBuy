from functools import wraps
import time
import traceback
from typing import List, Optional, Tuple
from fastapi import Request,status
from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel, Session, create_engine, delete, func, select
from app.db.models.inventory import INVENTORY, InventoryTableEnum
from app.db.models.item import ITEM, ItemTableEnum
from app.db.models.shop import SHOP, ShopTableEnum
from app.db.models.user import USER, USER_META, USER_SESSION, UserRole, UserTableEnum
from app.helpers import variables
from app.helpers.helpers import send_json_response
from app.helpers.variables import DATABASE_URL


class UninitializedDatabasePoolError(Exception):
    def __init__(
        self,
        message="The database connection pool has not been properly initialized.Please ensure setup is called",
    ):
        self.message = message
        super().__init__(self.message)


class DataBasePool:
    _db_pool: Session = None
    _engine = None

    @classmethod
    async def initDB(cls):
        # print(f"init database............ {cls._engine}")
        initDB(cls._engine)

    @classmethod
    async def getEngine(cls):
        return cls._engine

    @classmethod
    async def setup(cls, timeout: Optional[float] = None):
        if cls._engine != None:
            print(f"Droping engine")
            # cls._engine.dispose()
            # cls._db_pool.close()
            initDB(cls._engine)
        else:
            # print(f"Settingup database............")
            cls._engine = create_engine(
                DATABASE_URL, pool_size=20, pool_pre_ping=True, pool_recycle=60
            )
            initDB(cls._engine)
            cls._timeout = timeout
            with Session(cls._engine) as session:
                cls._db_pool = session
            # print(f"db setup done")

    @classmethod
    async def get_pool(cls) -> Session:
        if not cls._db_pool:
            raise UninitializedDatabasePoolError()
        return cls._db_pool

    @classmethod
    async def teardown(cls):
        print(f"Closing db_pool")
        if not cls._db_pool:
            raise UninitializedDatabasePoolError()
        cls._db_pool.close()
        print(f"db_pool closed")


def initDB(_engine):
    try:
        # print(f"_engine {_engine} capsonic")
        SQLModel.metadata.create_all(_engine)
        pass
    except:
        traceback.print_exc()
        print(f"Error in creating init tables.")


class DB:
    def __init__(self):
        pass
    
    @classmethod
    async def get_user(cls, data: int | str, db_pool: Session):
        try:
            if isinstance(data, int):
                statement = select(USER).where(USER.id == data)
            else:
                statement = select(USER).where(USER.email == data)
            
            user = db_pool.exec(statement).first()
            return user
        
        except Exception as e:
            print(f"Exception in get_user: {str(e)}")
            traceback.print_exc()
            db_pool.rollback()
            return None
        
    @classmethod
    async def getUserSession(self, db_pool, session_token):
            try:
                statement = select(USER_SESSION).where(USER_SESSION.pk == session_token)
                user_session = db_pool.exec(statement).first()
                # print(f"user {USER_SESSION}")
                if user_session:
                    return user_session
            except:
                return None

    @classmethod
    async def insert(self, dbClassNam: str, data: dict, db_pool: Session, commit: bool = False):
        try:
            if dbClassNam == UserTableEnum.USER:
                data = USER(**data)
            elif dbClassNam == UserTableEnum.USER_SESSION:
                data = USER_SESSION(**data)
            elif dbClassNam == UserTableEnum.USER_META:
                data = USER_META(**data)
            elif dbClassNam == ItemTableEnum.ITEM:
                data = ITEM(**data)
            elif dbClassNam == ShopTableEnum.SHOP:
                data = SHOP(**data)
            elif dbClassNam == InventoryTableEnum.INVENTORY:
                data = INVENTORY(**data)
            else:
                return None, False

            db_pool.add(data)
            if commit:
                db_pool.commit()
                db_pool.refresh(data)

            return data, True
        except:
            db_pool.rollback()
            traceback.print_exc()
            return None, False

    @classmethod
    async def delete(self, data, db_pool):
        try:
            db_pool.delete(data)
            # db_pool.commit()
            return True
        except:
            db_pool.rollback()
            traceback.print_exc()
            return False
        
    @classmethod
    async def delete_session_by_token(cls, db_pool, session_token: str):
        try:
            stmt = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
            db_pool.exec(stmt)
            db_pool.commit()
            return True
        except Exception:
            db_pool.rollback()
            traceback.print_exc()
            return False


    # @classmethod
    # async def get_item_by_name(self, itemName: str, db_pool: Session):
    #     try:
    #         statement = select(ITEM).where(ITEM.itemName == itemName)
    #         item = db_pool.exec(statement).first()
    #         return item
    #     except Exception as e:
    #         print(f"Exception in get_item_by_name: {str(e)}")
    #         traceback.print_exc()
    #         return None
        
    
    @classmethod
    async def get_attr_all(self, dbClassNam: str, db_pool: Session, filters: dict = None, all=True):
        try:
            models = {
                ItemTableEnum.ITEM: ITEM,
                UserTableEnum.USER: USER,
                UserTableEnum.USER_META: USER_META,
                UserTableEnum.USER_SESSION: USER_SESSION,
                ShopTableEnum.SHOP: SHOP,
                InventoryTableEnum.INVENTORY: INVENTORY,
            }

            table = models.get(dbClassNam)
            if not table:
                return None
            
            statement = select(table)

            if filters and isinstance(filters, dict):
                for key, value in filters.items():
                    if hasattr(table, key):
                        column_attr = getattr(table, key)
                        if isinstance(value, list):
                            statement = statement.where(column_attr.in_(value))
                        elif value is None:
                            statement = statement.where(column_attr.is_(None))
                        else:
                            statement = statement.where(column_attr == value)
            if all:
                result = db_pool.exec(statement).all()
            else:
                result = db_pool.exec(statement).first()
            return result
        
        except Exception as e:
            traceback.print_exc()
            if isinstance(db_pool, Session):
                db_pool.rollback()
            return None
        
    @classmethod
    async def update_attr_all(cls, dbClassNam: str, data: dict, db_pool: Session, identifier: dict):
        try:
            table_map = {
                ItemTableEnum.ITEM: ITEM,
                UserTableEnum.USER: USER,
                UserTableEnum.USER_META: USER_META,
                UserTableEnum.USER_SESSION: USER_SESSION,
                ShopTableEnum.SHOP: SHOP,
                InventoryTableEnum.INVENTORY: INVENTORY,

                
            }

            table_class = table_map.get(dbClassNam)
            if not table_class:
                message = "Invalid table class name provided."
                return message, False

            statement = select(table_class)
            for key, value in identifier.items():
                if hasattr(table_class, key):
                    statement = statement.where(getattr(table_class, key) == value)

            record = db_pool.exec(statement).first()
            if not record:
                message = "Not found."
                return message, False

            # Check if all values are the same
            all_same = True
            for key, value in data.items():
                if hasattr(record, key):
                    if getattr(record, key) != value:
                        all_same = False
                        break

            if all_same:
                message = "All values are the same, no update needed."
                return message, False

            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)

            db_pool.commit()
            message = "Updated successfully."
            return message, True

        except Exception:
            db_pool.rollback()
            traceback.print_exc()
            message = "Error updating."
            return message, False

    @classmethod
    async def delete_attr(cls, dbClassNam: str, db_pool: Session, identifier: dict):
        try:
            table_map = {
                ItemTableEnum.ITEM: ITEM,
                UserTableEnum.USER: USER,
                UserTableEnum.USER_META: USER_META,
                UserTableEnum.USER_SESSION: USER_SESSION,
                ShopTableEnum.SHOP: SHOP,
                InventoryTableEnum.INVENTORY: INVENTORY,


            }

            table_class = table_map.get(dbClassNam)
            if not table_class:
                message = "Invalid table class name provided."
                return message, False

            statement = select(table_class)
            for key, value in identifier.items():
                if hasattr(table_class, key):
                    statement = statement.where(getattr(table_class, key) == value)

            record = db_pool.exec(statement).first()
            if not record:
                message = "Not found."
                return message, False

            db_pool.delete(record)
            db_pool.commit()
            message = "Deleted successfully."
            return message, True

        except Exception:
            db_pool.rollback()
            traceback.print_exc()
            message = "Error deleting."
            return message, False

    @classmethod  
    async def get_attr_all_paginated(cls,dbClassNam,db_pool,offset: int = 0,limit: int = 20,filters: Optional[List] = None,order_by: Optional[List] = None) -> Tuple[List[dict], int]:
        try:
            session = db_pool
            query = select(dbClassNam)
            count_query = select(func.count()).select_from(dbClassNam)

            if filters:
                for f in filters:
                    query = query.where(f)
                    count_query = count_query.where(f)

            if order_by:
                query = query.order_by(*order_by)

            query = query.offset(offset).limit(limit)
            result = session.execute(query)
            rows = result.scalars().all()

            count_result = session.execute(count_query)
            total_count = count_result.scalar_one()

            return [jsonable_encoder(row) for row in rows], total_count
        except Exception as e:
            print("Exception in get_attr_all_paginated:", str(e))
            traceback.print_exc()
            return [], 0


# def authentication_required(func):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         try:
#             db_pool: Optional[Session] = kwargs.get("db_pool", None)
#             request: Request = kwargs.get("request")

#             if not request:
#                 return send_json_response(message="Unable to process authentication.", status=status.HTTP_400_BAD_REQUEST, body={})
#             session_token: Optional[str] = request.cookies.get(variables.COOKIE_KEY, None)
#             if not session_token:
#                 return send_json_response(message="Authentication token not provided.", status=status.HTTP_401_UNAUTHORIZED, body={})

#             if db_pool:
#                 user_session = await DB.getUserSession(db_pool, session_token)
#                 if not user_session:
#                     return send_json_response(message="Session expired or invalid. Please login again.", status=status.HTTP_401_UNAUTHORIZED, body={})

#                 if int(time.time()) > user_session.expired_at:
#                     statement = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
#                     db_pool.exec(statement)
#                     db_pool.commit()
#                     return send_json_response(message="Session expired. Please login again.", status=status.HTTP_401_UNAUTHORIZED, body={})
#                 kwargs["request"].state.emp = user_session 
#         except Exception as e:
#             print("Exception caught at authentication wrapper: ", str(e))
#             if db_pool:
#                 db_pool.rollback()  
#             traceback.print_exc()
#             return send_json_response(message="Error during authentication.", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
#         return await func(*args, **kwargs) 
#     return wrapper

def authentication_required(allowed_roles: List[UserRole]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db_pool: Optional[Session] = kwargs.get("db_pool", None)
            request: Request = kwargs.get("request")
            try:
                if not request:
                    return send_json_response(
                        message="Unable to process authentication.",
                        status=status.HTTP_400_BAD_REQUEST, body={}
                    )
                session_token: Optional[str] = request.cookies.get(variables.COOKIE_KEY, None)
                if not session_token:
                    return send_json_response(
                        message="Authentication token not provided.",
                        status=status.HTTP_401_UNAUTHORIZED, body={}
                    )

                if db_pool:
                    user_session = await DB.getUserSession(db_pool, session_token)
                    if not user_session:
                        return send_json_response(
                            message="Session expired or invalid. Please login again.",
                            status=status.HTTP_401_UNAUTHORIZED, body={}
                        )

                    if int(time.time()) > user_session.expired_at:
                        from sqlalchemy import delete
                        statement = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
                        db_pool.exec(statement)
                        db_pool.commit()
                        return send_json_response(
                            message="Session expired. Please login again.",
                            status=status.HTTP_401_UNAUTHORIZED, body={}
                        )

                    user_role = getattr(user_session, "role", None)
                    
                    if user_role is None and isinstance(user_session, dict) and "role" in user_session:
                        user_role = user_session["role"]
                    if user_role is None:
                        return send_json_response(message="No user role found.",status=status.HTTP_403_FORBIDDEN, body={})
                    
                    user_role_str = user_role.value.upper() if isinstance(user_role, UserRole) else str(user_role).upper()
                    allowed_values = [
                        r.value.upper() if isinstance(r, UserRole) else str(r).upper()
                        for r in allowed_roles
                    ]
                    # print("DEBUG: user_role_str =", user_role_str, "allowed =", allowed_values)
                    if user_role_str not in allowed_values:
                        return send_json_response(message="You do not have permission to access this resource.",status=status.HTTP_403_FORBIDDEN, body={})
                    kwargs["request"].state.emp = user_session
            except Exception as e:
                # print("Exception caught at authentication wrapper: ", str(e))
                if db_pool:
                    db_pool.rollback()
                traceback.print_exc()
                return send_json_response(message="Error during authentication.",status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def ADMIN_AUTHENTICATION_ONLY(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            db_pool: Optional[Session] = kwargs.get("db_pool", None)
            request: Request = kwargs.get("request")
            if not request:
                return send_json_response(message="Unable to process authentication.", status=status.HTTP_400_BAD_REQUEST, body={})
            session_token: Optional[str] = request.cookies.get(variables.COOKIE_KEY, None)
            if not session_token:
                return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})
            if db_pool:
                user_session = await DB.getUserSession(db_pool, session_token)
                if not user_session:
                    return send_json_response(message="Session expired or invalid. Please login again.", status=status.HTTP_401_UNAUTHORIZED, body={})
                if int(time.time()) > user_session.expired_at:
                    statement = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
                    db_pool.exec(statement)
                    db_pool.commit()
                    return send_json_response(message="Session expired. Please login again.", status=status.HTTP_401_UNAUTHORIZED, body={})
                if user_session.role != UserRole.ADMIN: 
                    return send_json_response(message="Insufficient privileges.", status=status.HTTP_403_FORBIDDEN, body={})
                kwargs["request"].state.emp = user_session
        except Exception as e:
            print("Exception caught at admin authentication wrapper: ", str(e))
            if db_pool:
                db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="Error during authentication.", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
        return await func(*args, **kwargs)
    return wrapper