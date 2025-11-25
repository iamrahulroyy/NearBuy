import sys
import os
import asyncio
from sqlmodel import Session, create_engine

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.helpers.fake_data_generator import generate_fake_data
from app.helpers.variables import DATABASE_URL

def run_fake_data_generation():
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        generate_fake_data(session, num_shops=10, items_per_shop=5)

if __name__ == "__main__":
    run_fake_data_generation()
