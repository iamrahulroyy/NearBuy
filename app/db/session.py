from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

from app.helpers import variables

load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = variables.DATABASE_URL


engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
