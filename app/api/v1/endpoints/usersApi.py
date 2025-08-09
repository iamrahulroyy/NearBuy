from fastapi import APIRouter, Depends, Request
from app.api.v1.endpoints.auth.login import check_auth_status, login
from app.api.v1.endpoints.auth.logout import logout
from app.api.v1.endpoints.auth.register import contributor_signup, user_signup, vendor_signup
from app.api.v1.endpoints.functions.users import UDB
from app.core.limiter import limiter  
from app.db.models.user import UserRole
from app.db.schemas.user import Login_User, Register_STATE_CONTRIBUTER, Register_User, Register_Vendor
from app.db.session import DB, DataBasePool, authentication_required


user_router = APIRouter(prefix="/users", tags=["Users"])
udb = UDB() 

@user_router.post("/signup/user")
async def signup_user_endpoint(request: Request, data: Register_User, db_pool=Depends(DataBasePool.get_pool)):
    return await user_signup(request, data, db_pool)

@user_router.post("/signup/vendor")
async def signup_vendor_endpoint(request: Request, data: Register_Vendor, db_pool=Depends(DataBasePool.get_pool)):
    return await vendor_signup(request, data, db_pool)

@user_router.post("/signup/contributor")
async def signup_contributor_endpoint(request: Request, data: Register_STATE_CONTRIBUTER, db_pool=Depends(DataBasePool.get_pool)):
    return await contributor_signup(request, data, db_pool)

@user_router.post("/login", description="login endpoint for all")
@limiter.limit("5/minute")
async def unified_login(request: Request, data: Login_User, db_pool=Depends(DataBasePool.get_pool)):
    return await login(request, data, db_pool)
    
@user_router.post("/logout")
@authentication_required([UserRole.USER,UserRole.VENDOR,UserRole.ADMIN,UserRole.STATE_CONTRIBUTER])
async def unified_logout(request: Request,db_pool=Depends(DataBasePool.get_pool)):
    return await logout(request, db_pool)

@user_router.get("/auth", name="Check User Logged Status")
@authentication_required([UserRole.USER, UserRole.VENDOR, UserRole.ADMIN, UserRole.STATE_CONTRIBUTER])
async def unified_check_auth(request: Request,db_pool=Depends(DataBasePool.get_pool)):
    return await check_auth_status(request,db_pool)