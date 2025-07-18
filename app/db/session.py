from functools import wraps
import time
import traceback
from typing import Optional
from fastapi import Request,status
from sqlmodel import SQLModel, Session, create_engine, delete, select
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
    async def insert(self, dbClassNam: str, data: dict, db_pool: Session, commit: bool = True):
        try:
            if dbClassNam == UserTableEnum.USER:
                data = USER(**data)
            elif dbClassNam == UserTableEnum.USER_SESSION:
                data = USER_SESSION(**data)
            elif dbClassNam == UserTableEnum.USER_META:
                data = USER_META(**data)
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
            db_pool.commit()
            return True
        except:
            db_pool.rollback()
            traceback.print_exc()
            return False



def authentication_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            db_pool: Optional[Session] = kwargs.get("db_pool", None)
            request: Request = kwargs.get("request")

            if not request:
                return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})
            session_token: Optional[str] = request.cookies.get(variables.COOKIE_KEY, None)
            if not session_token:
                return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})

            if db_pool:
                user_session = await DB.getUserSession(db_pool, session_token)
                if not user_session:
                    return send_json_response(message="Session expired/invalid, please login again", status=status.HTTP_403_FORBIDDEN, body={})

                if int(time.time()) > user_session.expired_at:
                    statement = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
                    db_pool.exec(statement)
                    db_pool.commit()
                    return send_json_response(message="Session expired/invalid, please login again", status=status.HTTP_403_FORBIDDEN, body={})
                kwargs["request"].state.emp = user_session 
        except Exception as e:
            print("Exception caught at authentication wrapper: ", str(e))
            if db_pool:
                db_pool.rollback()  
            traceback.print_exc()
            return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})
        return await func(*args, **kwargs) 
    return wrapper

def ADMIN_AUTHENTICATION_ONLY(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            db_pool: Optional[Session] = kwargs.get("db_pool", None)
            request: Request = kwargs.get("request")
            if not request:
                return send_json_response(message="Authentication token not provided", status=status.HTTP_403_FORBIDDEN, body={})
            session_token: Optional[str] = request.cookies.get(variables.COOKIE_KEY, None)
            if not session_token:
                return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})
            if db_pool:
                user_session = await DB.getUserSession(db_pool, session_token)
                if not user_session:
                    return send_json_response(message="Session expired/invalid, please login again.", status=status.HTTP_403_FORBIDDEN, body={})
                if int(time.time()) > user_session.expired_at:
                    statement = delete(USER_SESSION).where(USER_SESSION.pk == session_token)
                    db_pool.exec(statement)
                    db_pool.commit()
                    return send_json_response(message="Session expired/invalid, please login again.", status=status.HTTP_403_FORBIDDEN, body={})
                if user_session.role != UserRole.ADMIN: 
                    return send_json_response(message="Access forbidden: Insufficient privileges.", status=status.HTTP_403_FORBIDDEN, body={})
                kwargs["request"].state.emp = user_session
        except Exception as e:
            print("Exception caught at admin authentication wrapper: ", str(e))
            if db_pool:
                db_pool.rollback()
            traceback.print_exc()
            return send_json_response(message="Authentication token not provided.", status=status.HTTP_403_FORBIDDEN, body={})
        return await func(*args, **kwargs)
    return wrapper