import traceback
from fastapi import Request,status
from sqlmodel import Session
from app.db.session import DB
from app.helpers import variables
from app.helpers.helpers import send_json_response

uDB = DB()

async def logout(request:Request, db_pool: Session):
    try:
        await uDB.delete(request.state.emp, db_pool)

        db_pool.commit()

        response = send_json_response(message="Logged out successfully",status=status.HTTP_200_OK,body={})
        response.delete_cookie(key=variables.COOKIE_KEY)
        return response
    except Exception as e:
        traceback.print_exc()
        return send_json_response(message="Logout Failed",status=status.HTTP_401_UNAUTHORIZED,body={})