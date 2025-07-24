import time
import traceback
import uuid
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.models.user import ReasonEnum, UserTableEnum
from app.db.schemas.user import Login_User
from app.db.session import DB
from app.helpers import variables
from app.helpers.helpers import get_fastApi_req_data, send_json_response
from app.helpers.loginHelper import security

uDB = DB()

from app.db.models.user import UserRole

async def login(request: Request, data: Login_User, db_pool: Session):
    try:
        apiData = await get_fastApi_req_data(request)
        if not data.email:
            return send_json_response(
                message="Invalid credentials",
                status=status.HTTP_401_UNAUTHORIZED,
                body={}
            )

        user_data = data.email.lower()
        user = await uDB.get_user(user_data, db_pool)
        if not user:
            return send_json_response(
                message="Account not found",
                status=status.HTTP_401_UNAUTHORIZED,
                body={}
            )

        if not security().verify_password(user.password, data.password):
            return send_json_response(
                message="Invalid credentials",
                status=status.HTTP_401_UNAUTHORIZED,
                body={}
            )

        token = str(uuid.uuid4())
        if data.keepLogin:
            max_age = 3600 * 24 * 30
        else:
            max_age = 3600 * 90
        expiry = int(time.time() + max_age)

        # >>> CORRECT WAY <<<
        role_value = user.role.value if isinstance(user.role, UserRole) else str(user.role)

        session_data = {
            "pk": token,
            "email": user.email,
            "ip": apiData.ip,
            "browser": apiData.browser,
            "os": apiData.os,
            "created_at": int(time.time()),
            "expired_at": expiry,
            "role": role_value             
        }
        print("Login: session role =", session_data["role"])

        session, ok = await uDB.insert(dbClassNam=UserTableEnum.USER_SESSION, data=session_data, db_pool=db_pool)

        USER_META = {
            "email": user.email,
            "reason": ReasonEnum.LOGIN,
            "ip": apiData.ip,
            "role": role_value,             
            "browser": apiData.browser,
            "os": apiData.os
        }
        await uDB.insert(dbClassNam=UserTableEnum.USER_META, data=USER_META, db_pool=db_pool)
        db_pool.commit()

        response = send_json_response(
            message="User logged in successfully",
            status=status.HTTP_200_OK,
            body=[]
        )
        response.set_cookie(
            key=variables.COOKIE_KEY,
            value=token,
            max_age=max_age,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return response
    except Exception as e:
        print("Exception caught at User Signin: ", str(e))
        traceback.print_exc()
        return send_json_response(
            message="Login Failed",
            status=status.HTTP_401_UNAUTHORIZED,
            body={}
        )


async def check_auth_status(request: Request, db_pool: Session):
    try:
        user = request.state.emp
        
        user_info = jsonable_encoder(user)
        sensitive_fields = ["password", "try_count", "updated_at"]
        for field in sensitive_fields:
            user_info.pop(field, None)
            
        return send_json_response(
            message="Session is valid.",
            status=status.HTTP_200_OK,
            body=user_info
        )
        
    except Exception as e:
        print(f"Exception caught at checking user logged state: {e}")
        traceback.print_exc()
        return send_json_response(
            message="Failed to process user auth status.",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            body={}
        )