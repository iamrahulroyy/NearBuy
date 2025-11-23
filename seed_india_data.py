import asyncio
import uuid
import random
from sqlmodel import select
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.models.user import USER, UserRole
from app.db.session import DataBasePool
from app.helpers.loginHelper import security

# India Data: States and major cities with approximate lat/lon
INDIA_DATA = {
    "Andhra Pradesh": {"Visakhapatnam": (17.6868, 83.2185), "Vijayawada": (16.5062, 80.6480)},
    "Arunachal Pradesh": {"Itanagar": (27.0844, 93.6053)},
    "Assam": {"Guwahati": (26.1445, 91.7362)},
    "Bihar": {"Patna": (25.5941, 85.1376)},
    "Chhattisgarh": {"Raipur": (21.2514, 81.6296)},
    "Goa": {"Panaji": (15.4909, 73.8278)},
    "Gujarat": {"Ahmedabad": (23.0225, 72.5714), "Surat": (21.1702, 72.8311)},
    "Haryana": {"Gurugram": (28.4595, 77.0266), "Faridabad": (28.4089, 77.3178)},
    "Himachal Pradesh": {"Shimla": (31.1048, 77.1734)},
    "Jharkhand": {"Ranchi": (23.3441, 85.3096)},
    "Karnataka": {"Bangalore": (12.9716, 77.5946), "Mysore": (12.2958, 76.6394)},
    "Kerala": {"Kochi": (9.9312, 76.2673), "Thiruvananthapuram": (8.5241, 76.9366)},
    "Madhya Pradesh": {"Bhopal": (23.2599, 77.4126), "Indore": (22.7196, 75.8577)},
    "Maharashtra": {"Mumbai": (19.0760, 72.8777), "Pune": (18.5204, 73.8567), "Nagpur": (21.1458, 79.0882)},
    "Manipur": {"Imphal": (24.8170, 93.9368)},
    "Meghalaya": {"Shillong": (25.5788, 91.8933)},
    "Mizoram": {"Aizawl": (23.7271, 92.7176)},
    "Nagaland": {"Kohima": (25.6751, 94.1086)},
    "Odisha": {"Bhubaneswar": (20.2961, 85.8245)},
    "Punjab": {"Ludhiana": (30.9010, 75.8573), "Amritsar": (31.6340, 74.8723)},
    "Rajasthan": {"Jaipur": (26.9124, 75.7873), "Udaipur": (24.5854, 73.7125)},
    "Sikkim": {"Gangtok": (27.3314, 88.6138)},
    "Tamil Nadu": {"Chennai": (13.0827, 80.2707), "Coimbatore": (11.0168, 76.9558)},
    "Telangana": {"Hyderabad": (17.3850, 78.4867)},
    "Tripura": {"Agartala": (23.8315, 91.2868)},
    "Uttar Pradesh": {"Lucknow": (26.8467, 80.9462), "Varanasi": (25.3176, 82.9739), "Noida": (28.5355, 77.3910)},
    "Uttarakhand": {"Dehradun": (30.3165, 78.0322)},
    "West Bengal": {"Kolkata": (22.5726, 88.3639)},
    "Andaman and Nicobar Islands": {"Port Blair": (11.6234, 92.7265)},
    "Chandigarh": {"Chandigarh": (30.7333, 76.7794)},
    "Dadra and Nagar Haveli and Daman and Diu": {"Daman": (20.3974, 72.8328)},
    "Delhi": {"New Delhi": (28.6139, 77.2090)},
    "Jammu and Kashmir": {"Srinagar": (34.0837, 74.7973)},
    "Ladakh": {"Leh": (34.1526, 77.5770)},
    "Lakshadweep": {"Kavaratti": (10.5667, 72.6417)},
    "Puducherry": {"Puducherry": (11.9416, 79.8083)}
}

SHOP_TYPES = [
    ("Electronics", "Gadgets & Gear", "Best electronics in town"),
    ("Fashion", "Trends & Threads", "Latest fashion apparel"),
    ("Grocery", "Daily Fresh", "Fresh groceries daily"),
    ("Handicrafts", "Artisan's Corner", "Authentic handmade items"),
    ("Books", "Readers Paradise", "Books for every reader"),
    ("Furniture", "Comfort Living", "Modern and classic furniture"),
    ("Sports", "Active Life", "Sports equipment and gear")
]

ITEM_TEMPLATES = {
    "Electronics": [("Smartphone", 15000), ("Laptop", 45000), ("Headphones", 2000), ("Smartwatch", 3500)],
    "Fashion": [("T-Shirt", 500), ("Jeans", 1200), ("Saree", 2500), ("Sneakers", 1800)],
    "Grocery": [("Rice (5kg)", 300), ("Wheat Flour (5kg)", 250), ("Cooking Oil (1L)", 150), ("Spices Pack", 100)],
    "Handicrafts": [("Pottery Vase", 800), ("Handwoven Rug", 3000), ("Wooden Toy", 400), ("Brass Lamp", 1200)],
    "Books": [("Fiction Novel", 400), ("Notebook Set", 150), ("Pen Set", 100), ("Art Supplies", 600)],
    "Furniture": [("Study Table", 3500), ("Office Chair", 4500), ("Bookshelf", 2500), ("Bean Bag", 1500)],
    "Sports": [("Cricket Bat", 2500), ("Football", 800), ("Yoga Mat", 600), ("Dumbbells (Pair)", 1200)]
}

async def seed_data():
    await DataBasePool.setup()
    db_pool = DataBasePool._db_pool
    
    if db_pool is None:
        print("Database pool is not initialized.")
        return

    print("Starting data seeding for India...")

    for state, cities in INDIA_DATA.items():
        for city, (base_lat, base_lon) in cities.items():
            print(f"Seeding data for {city}, {state}...")
            
            # Create 3-5 shops per city
            num_shops = random.randint(3, 5)
            
            for i in range(num_shops):
                shop_type, shop_name_suffix, shop_desc_suffix = random.choice(SHOP_TYPES)
                
                # Randomize location slightly around the city center (approx within 5-10km)
                lat_offset = random.uniform(-0.05, 0.05)
                lon_offset = random.uniform(-0.05, 0.05)
                shop_lat = base_lat + lat_offset
                shop_lon = base_lon + lon_offset
                
                shop_name = f"{city} {shop_name_suffix} {i+1}"
                owner_email = f"owner_{city.lower().replace(' ', '')}_{i+1}@example.com"
                
                # 1. Create Vendor User
                statement = select(USER).where(USER.email == owner_email)
                existing_user = db_pool.exec(statement).first()
                
                if not existing_user:
                    owner_id = uuid.uuid4()
                    vendor_user = USER(
                        id=owner_id,
                        email=owner_email,
                        password=security().hash_password("Password@123"),
                        fullName=f"Owner {shop_name}",
                        role=UserRole.VENDOR
                    )
                    db_pool.add(vendor_user)
                    # print(f"  Created user: {owner_email}")
                else:
                    owner_id = existing_user.id
                    # print(f"  User exists: {owner_email}")

                # 2. Create Shop
                # Check if shop exists by name and owner (simplified check)
                statement = select(SHOP).where(SHOP.shopName == shop_name, SHOP.owner_id == owner_id)
                existing_shop = db_pool.exec(statement).first()
                
                if not existing_shop:
                    shop_id = uuid.uuid4()
                    shop = SHOP(
                        shop_id=shop_id,
                        owner_id=owner_id,
                        fullName=f"Owner {shop_name}",
                        shopName=shop_name,
                        address=f"Shop {i+1}, {city}, {state}",
                        contact=f"+91-{random.randint(7000000000, 9999999999)}",
                        description=f"{shop_desc_suffix} in {city}.",
                        is_open=True,
                        latitude=shop_lat,
                        longitude=shop_lon
                    )
                    db_pool.add(shop)
                    # print(f"  Created shop: {shop_name}")
                else:
                    shop_id = existing_shop.shop_id
                    existing_shop.latitude = shop_lat
                    existing_shop.longitude = shop_lon
                    db_pool.add(existing_shop)
                    # print(f"  Shop exists: {shop_name}")

                # 3. Create Items for the Shop
                items = ITEM_TEMPLATES.get(shop_type, [])
                # Add 2-4 items per shop
                selected_items = random.sample(items, min(len(items), random.randint(2, 4)))
                
                for item_name, base_price in selected_items:
                    statement = select(ITEM).where(ITEM.itemName == item_name, ITEM.shop_id == shop_id)
                    existing_item = db_pool.exec(statement).first()
                    
                    if not existing_item:
                        price = base_price + random.randint(-100, 100) # Slight price variation
                        item = ITEM(
                            id=uuid.uuid4(),
                            shop_id=shop_id,
                            itemName=item_name,
                            price=float(price),
                            description=f"High quality {item_name} available at {shop_name}."
                        )
                        db_pool.add(item)
                        # print(f"    Added item: {item_name}")
    
    try:
        db_pool.commit()
        print("\n--- Seeding Complete! ---")
        print("Database populated with India-based data.")
    except Exception as e:
        print(f"Error committing to database: {e}")
        db_pool.rollback()

if __name__ == "__main__":
    asyncio.run(seed_data())
