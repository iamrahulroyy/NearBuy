#!/usr/bin/env python3
"""Clear all shops and items from database before re-seeding"""

import asyncio
from sqlmodel import select, delete
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.session import DataBasePool

async def clear_database():
    await DataBasePool.setup()
    db_pool = DataBasePool._db_pool
    
    if db_pool is None:
        print("Database pool is not initialized.")
        return
    
    print("Clearing existing data...")
    
    # Delete all items first (foreign key constraint)
    item_count = len(db_pool.exec(select(ITEM)).all())
    print(f"  Deleting {item_count} items...")
    db_pool.exec(delete(ITEM))
    
    # Delete all shops
    shop_count = len(db_pool.exec(select(SHOP)).all())
    print(f"  Deleting {shop_count} shops...")
    db_pool.exec(delete(SHOP))
    
    db_pool.commit()
    print("✅ Database cleared successfully!")

if __name__ == "__main__":
    asyncio.run(clear_database())
