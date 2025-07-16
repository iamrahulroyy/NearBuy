# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, select
# from app.db.queries import insert_instance
# from app.db.session import get_session
# from app.db.models.user import User
# from app.db.schemas.user import UserCreate, UserRead
# from uuid import uuid4
# import bcrypt

# user_router = APIRouter(prefix="/users", tags=["Users"])

# @user_router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def signup(user: UserCreate, session: Session = Depends(get_session)):
#     if session.exec(select(User).where(User.email == user.email)).first():
#         raise HTTPException(status_code=400, detail="Email already registered")
#     hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#     user_dict = user.model_dump()
#     user_dict.update({"id": uuid4(), "password": hashed_password})
#     return insert_instance(session, User, user_dict)

# @user_router.post("/login")
# def login(user: UserCreate, session: Session = Depends(get_session)):
#     db_user = session.exec(select(User).where(User.email == user.email)).first()
#     if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"message": "Login successful", "user_id": str(db_user.id)}
