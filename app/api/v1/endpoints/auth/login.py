import time
import traceback
import uuid
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.models.user import ReasonEnum, UserTableEnum
from app.db.schemas.user import Login_User
from app.db.session import DB
from app.helpers.helpers import get_fastApi_req_data, send_json_response
from app.helpers.loginHelper import security

uDB = DB()

async def login(request: Request, data: Login_User, db_pool: Session):
    try:
        apiData = await get_fastApi_req_data(request)
        if not data.email:
            return send_json_response(message="Invalid credentials", status=status.HTTP_401_UNAUTHORIZED, body={})
        
        user_data = data.email.lower()
        user = await uDB.get_user(user_data, db_pool)

        if not user:
            return send_json_response(message="Account not found", status=status.HTTP_401_UNAUTHORIZED, body={})
        
        serialized_inserted_user = jsonable_encoder(user)

        if not security().verify_password(user.password, data.password):
            return send_json_response(message="Invalid credentials", status=status.HTTP_401_UNAUTHORIZED, body={})

        token = str(uuid.uuid4())
        if data.keepLogin:
            max_age = 3600 * 24 * 30
        else:
            max_age = 3600 * 90
        expiry = int(time.time() + max_age)

        session_data = {"pk": token, "email": user.email, "ip": apiData.ip, "browser": apiData.browser,
                        "os": apiData.os, "created_at": int(time.time()), "expired_at": expiry, "role": user.role}
        session, ok = await uDB.insert(dbClassNam=UserTableEnum.USER_SESSION, data=session_data, db_pool=db_pool)

        USER_META = {
            "email": user.email, 
            "reason": ReasonEnum.LOGIN, 
            "ip": apiData.ip,
            "role": user.role,
            "browser": apiData.browser,
            "os": apiData.os
        }
        await uDB.insert(dbClassNam=UserTableEnum.USER_META, data=USER_META, db_pool=db_pool)

        response = send_json_response(message="User logged in successfully", status=status.HTTP_200_OK, body=[])
        return response
    except Exception as e:
        print("Exception caught at User Signin: ", str(e))
        traceback.print_exc()
        return send_json_response(message="Login Failed", status=status.HTTP_401_UNAUTHORIZED, body={})
