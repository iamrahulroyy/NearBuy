import uuid
import time
from sqlmodel import Session, select
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.models.user import USER, UserRole
from app.db.session import DataBasePool
from app.helpers.loginHelper import security
from app.helpers.geo import create_point_geometry

async def setup_db():
    await DataBasePool.setup()

def run():
    db_pool = DataBasePool._db_pool
    if db_pool is None:
        print("Database pool is not initialized.")
        return

    # --- Use the IDs you provided ---
    owner_id = uuid.UUID("3e592b3b-5064-4ff5-9fcf-2bf8382972fe")
    shop_id = uuid.UUID("07446c46-7775-4c99-a29e-79843fb69f93")
    vendor_email = "anita.verma@vermahandicrafts.com"

    # --- 1. Create or Find the Vendor User ---
    statement = select(USER).where(USER.id == owner_id)
    existing_user = db_pool.exec(statement).first()
    if not existing_user:
        vendor_user = USER(id=owner_id, email=vendor_email, password=security().hash_password("Anita@2024"), fullName="Anita Verma", role=UserRole.VENDOR)
        db_pool.add(vendor_user)
        print(f"Creating vendor user: {vendor_email}")
    else:
        print(f"Found existing vendor user: {vendor_email}")

    # --- 2. Create or Update the Shop with Location ---
    statement = select(SHOP).where(SHOP.shop_id == shop_id)
    existing_shop = db_pool.exec(statement).first()
    
    # Define the location point
    shop_location = create_point_geometry(latitude=20.2961, longitude=85.8245)
    
    if not existing_shop:
        shop = SHOP(
            shop_id=shop_id,
            owner_id=owner_id,
            fullName="Anita Verma",
            shopName="Verma Handicrafts",
            address="45 MG Road, Sector 14, Gurugram, Haryana",
            contact="+91-9811122233",
            description="Authentic Indian handicrafts and textiles.",
            is_open=True,
            location=shop_location # Set location on creation
        )
        db_pool.add(shop)
        print(f"Creating shop: {shop.shopName} with location.")
    else:
        # If shop exists, UPDATE its location
        existing_shop.location = shop_location
        db_pool.add(existing_shop)
        print(f"Found existing shop. Updating location for: {existing_shop.shopName}")

    # --- 3. Create or Find an Item for the Shop ---
    item_name = "Hand-painted Silk Scarf"
    statement = select(ITEM).where(ITEM.itemName == item_name, ITEM.shop_id == shop_id)
    existing_item = db_pool.exec(statement).first()
    if not existing_item:
        item = ITEM(id=uuid.uuid4(), shop_id=shop_id, itemName=item_name, price=1250.00, description="A beautiful, one-of-a-kind silk scarf.")
        db_pool.add(item)
        print(f"Creating item: {item.itemName}")
    else:
        print(f"Found existing item: {existing_item.itemName}")

    # --- 4. Commit to Database ---
    db_pool.commit()
    print("\n--- Seeding Complete! ---")
    print("User, Shop, and Item are now correctly configured in the database.")
    print("-------------------------\n")


if __name__ == "__main__":
    import asyncio
    print("Starting database seeding...")
    asyncio.run(setup_db())
    run()