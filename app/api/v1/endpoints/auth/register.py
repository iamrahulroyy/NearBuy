import traceback
import time
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
from app.db.models.user import ReasonEnum, UserTableEnum, UserRole
from app.db.schemas.user import Register_STATE_CONTRIBUTER, Register_User, Register_Vendor
from app.db.session import DB
from app.helpers.helpers import get_fastApi_req_data, send_json_response
from app.helpers.loginHelper import security

uDB = DB()

async def user_signup(request: Request, data: Register_User, db_pool: Session):
    try:
        fullName = data.fullName.strip()
        email = data.email.lower()
        
        password = security().hash_password(data.password)
        
        if len(fullName) == 0:
            return send_json_response(message="Invalid fullName", status=status.HTTP_403_FORBIDDEN, body={})
        elif len(fullName) < 2 or len(fullName) > 50:
            return send_json_response(message="Full name should be between 2 and 50 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if not fullName.replace(" ", "").isalnum():
            return send_json_response(message="Only alphanumeric characters and spaces are allowed for full name", status=status.HTTP_403_FORBIDDEN, body={})
        
        if await uDB.get_user(email, db_pool):
            return send_json_response(message="Email already registered, Please try again", status=status.HTTP_403_FORBIDDEN, body={})
        
        apiData = await get_fastApi_req_data(request)
        
        USER_DATA = {
            "email": email,
            "password": password,
            "fullName": fullName,
            "role": UserRole.USER,
            "try_count": 0
        }
        
        inserted_user, ok = await uDB.insert(dbClassNam=UserTableEnum.USER, data=USER_DATA, db_pool=db_pool)
        
        if not ok or not inserted_user:
            return send_json_response(message="Could not create user account, please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
        
        serialized_inserted_user = jsonable_encoder(inserted_user)
        sensitive_fields = ["password", "try_count", "updated_at"]
        for field in sensitive_fields:
            serialized_inserted_user.pop(field, None)
        
        USER_META_DATA = {
            "email": email,
            "reason": ReasonEnum.SIGNUP,
            "browser": apiData.browser,
            "role": UserRole.USER,
            "os": apiData.os
        }
        
        await uDB.insert(dbClassNam=UserTableEnum.USER_META, data=USER_META_DATA, db_pool=db_pool)
        
        serialized_inserted_user.pop("id", None)

        db_pool.commit()
        return send_json_response(message="User registered successfully", status=status.HTTP_201_CREATED, body=serialized_inserted_user)
        
    except Exception as e:
        print("Exception caught at User Signup: ", str(e))
        traceback.print_exc()
        return send_json_response(message="Error during user signup process, please try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

async def vendor_signup(request: Request, data: Register_Vendor, db_pool: Session):
    try:
        fullName = data.fullName.strip()
        shopName = data.shopName.strip()
        address = data.address.strip()
        contact = data.contact.strip() if data.contact else None
        email = data.email.lower() if data.email else None
        
        if not email:
            return send_json_response(message="Email is required for vendor registration", status=status.HTTP_403_FORBIDDEN, body={})
        
        password = security().hash_password(data.password)
        
        if len(fullName) == 0:
            return send_json_response(message="Invalid fullName", status=status.HTTP_403_FORBIDDEN, body={})
        elif len(fullName) < 2 or len(fullName) > 50:
            return send_json_response(message="Full name should be between 2 and 50 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if len(shopName) == 0:
            return send_json_response(message="Invalid shop name", status=status.HTTP_403_FORBIDDEN, body={})
        elif len(shopName) < 2 or len(shopName) > 100:
            return send_json_response(message="Shop name should be between 2 and 100 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if len(address) == 0:
            return send_json_response(message="Invalid address", status=status.HTTP_403_FORBIDDEN, body={})
        elif len(address) < 5 or len(address) > 200:
            return send_json_response(message="Address should be between 5 and 200 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if contact and (len(contact) < 10 or len(contact) > 15):
            return send_json_response(message="Contact should be between 10 and 15 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if contact and not contact.replace("+", "").replace("-", "").replace(" ", "").isdigit():
            return send_json_response(message="Contact should only contain digits, +, -, and spaces", status=status.HTTP_403_FORBIDDEN, body={})
        
        if not fullName.replace(" ", "").isalnum():
            return send_json_response(message="Only alphanumeric characters and spaces are allowed for full name", status=status.HTTP_403_FORBIDDEN, body={})
        
        if await uDB.get_user(email, db_pool):
            return send_json_response(message="Email already registered, Please try again", status=status.HTTP_403_FORBIDDEN, body={})
        
        apiData = await get_fastApi_req_data(request)
        
        VENDOR_DATA = {
            "email": email,
            "password": password,
            "fullName": fullName,
            "role": UserRole.VENDOR,
            "try_count": 0,
            "note": f"Shop: {shopName}, Address: {address}, Contact: {contact}"
        }
        
        inserted_vendor, ok = await uDB.insert(dbClassNam=UserTableEnum.USER, data=VENDOR_DATA, db_pool=db_pool)
        
        if not ok or not inserted_vendor:
            return send_json_response(message="Could not create vendor account, please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
        
        serialized_inserted_vendor = jsonable_encoder(inserted_vendor)
        sensitive_fields = ["password", "try_count", "updated_at"]
        for field in sensitive_fields:
            serialized_inserted_vendor.pop(field, None)
        
        VENDOR_META_DATA = {
            "email": email,
            "reason": ReasonEnum.SIGNUP,
            "browser": apiData.browser,
            "role": UserRole.VENDOR,
            "os": apiData.os
        }
        
        await uDB.insert(dbClassNam=UserTableEnum.USER_META, data=VENDOR_META_DATA, db_pool=db_pool)
        
        serialized_inserted_vendor.pop("id", None)

        db_pool.commit()

        return send_json_response(message="Vendor registered successfully", status=status.HTTP_201_CREATED, body=serialized_inserted_vendor)
        
    except Exception as e:
        print("Exception caught at Vendor Signup: ", str(e))
        traceback.print_exc()
        return send_json_response(message="Error during vendor signup process, please try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})

async def contributor_signup(request: Request, data: Register_STATE_CONTRIBUTER, db_pool: Session):
    try:
        fullName = data.fullName.strip()
        email = data.email.lower()
        
        password = security().hash_password(data.password)
        
        if len(fullName) == 0:
            return send_json_response(message="Invalid fullName", status=status.HTTP_403_FORBIDDEN, body={})
        elif len(fullName) < 2 or len(fullName) > 50:
            return send_json_response(message="Full name should be between 2 and 50 characters", status=status.HTTP_403_FORBIDDEN, body={})
        
        if not fullName.replace(" ", "").isalnum():
            return send_json_response(message="Only alphanumeric characters and spaces are allowed for full name", status=status.HTTP_403_FORBIDDEN, body={})
        
        if await uDB.get_user(email, db_pool):
            return send_json_response(message="Email already registered, Please try again", status=status.HTTP_403_FORBIDDEN, body={})
        
        apiData = await get_fastApi_req_data(request)
        
        CONTRIBUTOR_DATA = {
            "email": email,
            "password": password,
            "fullName": fullName,
            "role": UserRole.STATE_CONTRIBUTER,
            "try_count": 0
        }
        
        inserted_contributor, ok = await uDB.insert(dbClassNam=UserTableEnum.USER, data=CONTRIBUTOR_DATA, db_pool=db_pool)
        
        if not ok or not inserted_contributor:
            return send_json_response(message="Could not create contributor account, please try again", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
        
        serialized_inserted_contributor = jsonable_encoder(inserted_contributor)
        sensitive_fields = ["password", "try_count", "updated_at"]
        for field in sensitive_fields:
            serialized_inserted_contributor.pop(field, None)
        
        CONTRIBUTOR_META_DATA = {
            "email": email,
            "reason": ReasonEnum.SIGNUP,
            "browser": apiData.browser,
            "role": UserRole.STATE_CONTRIBUTER,
            "os": apiData.os
        }
        
        await uDB.insert(dbClassNam=UserTableEnum.USER_META, data=CONTRIBUTOR_META_DATA, db_pool=db_pool)
        
        serialized_inserted_contributor.pop("id", None)

        db_pool.commit()
        return send_json_response(message="Contributor registered successfully", status=status.HTTP_201_CREATED, body=serialized_inserted_contributor)
        
    except Exception as e:
        print("Exception caught at Contributor Signup: ", str(e))
        traceback.print_exc()
        return send_json_response(message="Error during contributor signup process, please try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR, body={})
