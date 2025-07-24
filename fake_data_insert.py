import uuid
import time
import random
from sqlmodel import Session
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.models.inventory import INVENTORY, StockStatus  
from app.db.session import DataBasePool

def real_address():
    return random.choice([
        "12 Linking Road, Mumbai",
        "45 Church Street, Bengaluru",
        "18 Camac Street, Kolkata",
        "90 Janpath Road, Delhi",
        "34 Jubilee Hills, Hyderabad"
    ])

async def setup_db():
    await DataBasePool.setup()

def run():
    db_pool = DataBasePool._db_pool
    if db_pool is None:
        print("No db pool! Init your DB first.")
        return

    shop_uuid = uuid.uuid4()
    item_uuid = uuid.uuid4()
    inventory_uuid = str(uuid.uuid4())

    # Create a realistic shop
    shop = SHOP(
        shop_id=shop_uuid,
        owner_id=uuid.UUID("7ad811a9-2cea-4980-9e2f-fc86dc99ad29"),
        fullName="Ravi Sharma",
        shopName="FreshMart Grocery",
        address=real_address(),
        contact="982307" + str(random.randint(1000, 9999)),
        description="A modern grocery store offering fresh produce and daily essentials.",
        is_open=True,
        location=None,
        created_at=int(time.time()),
        note="Inserted by setup script"
    )

    # Create a realistic item
    item_price = round(random.uniform(150, 250), 2)
    item = ITEM(
        id=item_uuid,
        itemName="Organic Basmati Rice",
        price=item_price,
        description="Premium quality, aged basmati rice ideal for daily meals.",
        note="Added via initialization script"
    )

    with db_pool:
        # Add and flush shop & item
        db_pool.add(shop)
        db_pool.add(item)
        db_pool.flush()  # Required to insert SHOP and ITEM before referencing in INVENTORY

        # Insert inventory
        inventory = INVENTORY(
            inventory_id=inventory_uuid,
            shop_id=shop_uuid,
            item_id=item_uuid,
            quantity=random.randint(15, 40),
            price_at_entry=item_price,
            last_restocked_at=int(time.time()),
            min_quantity=5,
            max_quantity=100,
            status=StockStatus.IN_STOCK,
            location="Back Shelf A3",
            batch_number="BATCH" + str(random.randint(1000, 9999)),
            expiry_date=int(time.time()) + 60 * 60 * 24 * 180,  # 6 months later
            updated_at=int(time.time()),
            note="Initial stock added via script"
        )

        db_pool.add(inventory)
        db_pool.commit()

        db_pool.refresh(shop)
        db_pool.refresh(item)
        db_pool.refresh(inventory)

    print("Inserted shop:", shop.shop_id, shop.fullName)
    print("Inserted item:", item.id, item.itemName)
    print("Inserted inventory:", inventory.inventory_id, f"{inventory.quantity} units at ₹{inventory.price_at_entry}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup_db())
    run()

# ------------------- fake_data -------------------
# {
#   "fullName": "Neha Singh",
#   "email": "neha.singh@govstatsportal.in",
#   "password": "Neha@2024",
#   "role": "STATE_CONTRIBUTER"
# }
# {
#   "fullName": "Karan Mehta",
#   "email": "karan.mehta@examplemail.com",
#   "password": "Karan@1234",
#   "role": "USER"
# }
# {
#   "fullName": "Anita Verma",
#   "shopName": "Verma Handicrafts",
#   "address": "45 MG Road, Sector 14, Gurugram, Haryana",
#   "contact": "+91-9811122233",
#   "email": "anita.verma@vermahandicrafts.com",
#   "password": "Anita@2024",
#   "role": "VENDOR"
# }
