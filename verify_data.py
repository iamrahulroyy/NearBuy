import asyncio
from sqlmodel import select, func
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.session import DataBasePool

async def verify_data():
    await DataBasePool.setup()
    db_pool = DataBasePool._db_pool
    
    shop_count = db_pool.exec(select(func.count()).select_from(SHOP)).one()
    item_count = db_pool.exec(select(func.count()).select_from(ITEM)).one()
    
    print(f"Total Shops: {shop_count}")
    print(f"Total Items: {item_count}")

if __name__ == "__main__":
    asyncio.run(verify_data())
