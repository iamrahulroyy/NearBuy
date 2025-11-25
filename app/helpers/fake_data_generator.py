from typing import List, Dict, Any
import random
import uuid
import time
from sqlmodel import Session, select
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.models.user import USER, UserRole
from app.helpers.loginHelper import security

# --- Comprehensive India Data ---
INDIA_DATA = {
    "Andhra Pradesh": {"Visakhapatnam": (17.6868, 83.2185), "Vijayawada": (16.5062, 80.6480), "Guntur": (16.3067, 80.4365), "Nellore": (14.4426, 79.9865)},
    "Arunachal Pradesh": {"Itanagar": (27.0844, 93.6053), "Tawang": (27.5861, 91.8594)},
    "Assam": {"Guwahati": (26.1445, 91.7362), "Silchar": (24.8333, 92.7789), "Dibrugarh": (27.4728, 94.9120)},
    "Bihar": {"Patna": (25.5941, 85.1376), "Gaya": (24.7914, 85.0002), "Bhagalpur": (25.2425, 87.0111), "Muzaffarpur": (26.1209, 85.3647)},
    "Chhattisgarh": {"Raipur": (21.2514, 81.6296), "Bhilai": (21.1938, 81.3509), "Bilaspur": (22.0797, 82.1409)},
    "Goa": {"Panaji": (15.4909, 73.8278), "Margao": (15.2832, 73.9862), "Vasco da Gama": (15.3991, 73.8125)},
    "Gujarat": {"Ahmedabad": (23.0225, 72.5714), "Surat": (21.1702, 72.8311), "Vadodara": (22.3072, 73.1812), "Rajkot": (22.3039, 70.8022)},
    "Haryana": {"Gurugram": (28.4595, 77.0266), "Faridabad": (28.4089, 77.3178), "Panipat": (29.3909, 76.9635), "Ambala": (30.3782, 76.7767)},
    "Himachal Pradesh": {"Shimla": (31.1048, 77.1734), "Manali": (32.2432, 77.1892), "Dharamshala": (32.2190, 76.3234)},
    "Jharkhand": {"Ranchi": (23.3441, 85.3096), "Jamshedpur": (22.8046, 86.2029), "Dhanbad": (23.7957, 86.4304)},
    "Karnataka": {"Bangalore": (12.9716, 77.5946), "Mysore": (12.2958, 76.6394), "Hubli": (15.3647, 75.1240), "Mangalore": (12.9141, 74.8560)},
    "Kerala": {"Kochi": (9.9312, 76.2673), "Thiruvananthapuram": (8.5241, 76.9366), "Kozhikode": (11.2588, 75.7804), "Thrissur": (10.5276, 76.2144)},
    "Madhya Pradesh": {"Bhopal": (23.2599, 77.4126), "Indore": (22.7196, 75.8577), "Gwalior": (26.2183, 78.1828), "Jabalpur": (23.1815, 79.9864)},
    "Maharashtra": {"Mumbai": (19.0760, 72.8777), "Pune": (18.5204, 73.8567), "Nagpur": (21.1458, 79.0882), "Nashik": (19.9975, 73.7898), "Aurangabad": (19.8762, 75.3433)},
    "Manipur": {"Imphal": (24.8170, 93.9368)},
    "Meghalaya": {"Shillong": (25.5788, 91.8933)},
    "Mizoram": {"Aizawl": (23.7271, 92.7176)},
    "Nagaland": {"Kohima": (25.6751, 94.1086), "Dimapur": (25.9060, 93.7272)},
    "Odisha": {"Bhubaneswar": (20.2961, 85.8245), "Cuttack": (20.4625, 85.8828), "Rourkela": (22.2604, 84.8536), "Puri": (19.8135, 85.8312)},
    "Punjab": {"Ludhiana": (30.9010, 75.8573), "Amritsar": (31.6340, 74.8723), "Jalandhar": (31.3260, 75.5762), "Patiala": (30.3398, 76.3869)},
    "Rajasthan": {"Jaipur": (26.9124, 75.7873), "Udaipur": (24.5854, 73.7125), "Jodhpur": (26.2389, 73.0243), "Kota": (25.2138, 75.8648)},
    "Sikkim": {"Gangtok": (27.3314, 88.6138)},
    "Tamil Nadu": {"Chennai": (13.0827, 80.2707), "Coimbatore": (11.0168, 76.9558), "Madurai": (9.9252, 78.1198), "Trichy": (10.7905, 78.7047), "Salem": (11.6643, 78.1460)},
    "Telangana": {"Hyderabad": (17.3850, 78.4867), "Warangal": (17.9689, 79.5941), "Nizamabad": (18.6725, 78.0941)},
    "Tripura": {"Agartala": (23.8315, 91.2868)},
    "Uttar Pradesh": {"Lucknow": (26.8467, 80.9462), "Varanasi": (25.3176, 82.9739), "Noida": (28.5355, 77.3910), "Kanpur": (26.4499, 80.3319), "Agra": (27.1767, 78.0081), "Meerut": (28.9845, 77.7064)},
    "Uttarakhand": {"Dehradun": (30.3165, 78.0322), "Haridwar": (29.9457, 78.1642), "Nainital": (29.3919, 79.4542)},
    "West Bengal": {"Kolkata": (22.5726, 88.3639), "Howrah": (22.5958, 88.2636), "Darjeeling": (27.0360, 88.2627), "Siliguri": (26.7271, 88.3953)},
    "Andaman and Nicobar Islands": {"Port Blair": (11.6234, 92.7265)},
    "Chandigarh": {"Chandigarh": (30.7333, 76.7794)},
    "Dadra and Nagar Haveli and Daman and Diu": {"Daman": (20.3974, 72.8328)},
    "Delhi": {"New Delhi": (28.6139, 77.2090)},
    "Jammu and Kashmir": {"Srinagar": (34.0837, 74.7973), "Jammu": (32.7266, 74.8570)},
    "Ladakh": {"Leh": (34.1526, 77.5770)},
    "Lakshadweep": {"Kavaratti": (10.5667, 72.6417)},
    "Puducherry": {"Puducherry": (11.9416, 79.8083)}
}

# --- Realistic Shop Names and Categories ---
SHOP_CATEGORIES = {
    "Electronics": [
        "Croma", "Reliance Digital", "Vijay Sales", "Sangeetha Mobiles", "Poorvika Mobiles", 
        "Lot Mobiles", "UniverCell", "Adishwar", "Girias", "Viveks", "Shah Electronics", 
        "Digital World", "Gadget Zone", "Tech Connect", "Future World"
    ],
    "Fashion": [
        "Shoppers Stop", "Lifestyle", "Pantaloons", "Westside", "Max Fashion", "Trends", 
        "Fabindia", "Manyavar", "W for Woman", "Biba", "Raymond", "Peter England", 
        "Allen Solly", "Van Heusen", "Louis Philippe", "Zara", "H&M"
    ],
    "Grocery": [
        "Big Bazaar", "D-Mart", "Reliance Fresh", "More Supermarket", "Spencer's", 
        "Nature's Basket", "Ratnadeep", "Heritage Fresh", "Nilgiris", "Easyday", 
        "24 Seven", "Lulu Hypermarket", "Star Bazaar", "Spar Hypermarket"
    ],
    "Pharmacy": [
        "Apollo Pharmacy", "MedPlus", "Wellness Forever", "Netmeds Offline", "Frank Ross", 
        "Guardian Pharmacy", "Sanjivani", "Noble Plus", "Tulsi Pharmacy", "Health & Glow"
    ],
    "Jewelry": [
        "Tanishq", "Kalyan Jewellers", "Malabar Gold & Diamonds", "Joyalukkas", "PC Jeweller", 
        "Senco Gold", "TBZ", "Bhima Jewellers", "GRT Jewellers", "Lalithaa Jewellery"
    ],
    "Books & Stationery": [
        "Crossword", "Sapna Book House", "Oxford Bookstore", "Higginbothams", "Starmark", 
        "Om Book Shop", "Bahrisons", "Kitab Khana", "Full Circle", "Title Waves"
    ],
    "Footwear": [
        "Bata", "Metro Shoes", "Mochi", "Khadim's", "Relaxo", "Paragon", "Liberty", 
        "Woodland", "Red Tape", "Sreeleathers"
    ]
}

# --- Varied Items per Category ---
ITEM_TEMPLATES = {
    "Electronics": [
        ("Apple iPhone 15", 79900, "Latest Apple smartphone with A16 Bionic chip."),
        ("Samsung Galaxy S24", 74999, "Flagship Android phone with AI features."),
        ("Sony WH-1000XM5", 26990, "Industry-leading noise canceling headphones."),
        ("Dell XPS 13", 115000, "Premium ultrabook with InfinityEdge display."),
        ("MacBook Air M2", 99900, "Supercharged by M2 chip, incredibly thin."),
        ("LG 55-inch 4K TV", 45000, "UHD Smart LED TV with AI ThinQ."),
        ("JBL Flip 6", 9999, "Portable waterproof bluetooth speaker."),
        ("iPad Air", 59900, "Versatile tablet with M1 chip."),
        ("Canon EOS R50", 65000, "Mirrorless camera for creators."),
        ("PlayStation 5", 54990, "Next-gen gaming console.")
    ],
    "Fashion": [
        ("Men's Slim Fit Shirt", 1299, "Cotton formal shirt for office wear."),
        ("Women's Kurta Set", 2499, "Embroidered festive kurta with palazzo."),
        ("Denim Jeans", 1999, "Classic blue denim, regular fit."),
        ("Running Shoes", 3499, "Lightweight shoes for daily running."),
        ("Leather Jacket", 4999, "Genuine leather biker jacket."),
        ("Summer Dress", 1599, "Floral print cotton dress."),
        ("Silk Saree", 8999, "Traditional Kanjivaram silk saree."),
        ("Aviator Sunglasses", 2999, "Classic style with UV protection."),
        ("Wrist Watch", 4500, "Analog watch with leather strap."),
        ("Backpack", 1200, "Water-resistant laptop backpack.")
    ],
    "Grocery": [
        ("Basmati Rice (5kg)", 650, "Premium aged basmati rice."),
        ("Whole Wheat Atta (10kg)", 450, "Chakki fresh whole wheat flour."),
        ("Toor Dal (1kg)", 160, "Unpolished organic toor dal."),
        ("Sunflower Oil (1L)", 140, "Refined sunflower oil for cooking."),
        ("Tata Tea Gold (500g)", 300, "Rich taste and aroma tea."),
        ("Nescafe Classic (200g)", 550, "100% pure instant coffee."),
        ("Almonds (500g)", 450, "Premium California almonds."),
        ("Dark Chocolate", 150, "Rich dark chocolate bar."),
        ("Honey (500g)", 300, "Pure natural honey."),
        ("Oats (1kg)", 190, "Rolled oats for healthy breakfast.")
    ],
    "Pharmacy": [
        ("Paracetamol 650mg", 30, "Fever and pain relief tablets."),
        ("Multivitamin Supplements", 450, "Daily essential vitamins and minerals."),
        ("Whey Protein (1kg)", 2500, "Chocolate flavor muscle recovery protein."),
        ("Digital Thermometer", 250, "Quick and accurate temperature reading."),
        ("Face Mask (N95)", 100, "Protective face mask."),
        ("Hand Sanitizer (500ml)", 200, "Alcohol-based hand sanitizer."),
        ("Band-Aid Pack", 50, "Adhesive bandages for cuts."),
        ("Cough Syrup", 120, "Herbal relief for cough and cold."),
        ("Vitamin C Tablets", 300, "Immunity booster supplements."),
        ("Blood Pressure Monitor", 1800, "Automatic digital BP monitor.")
    ],
    "Jewelry": [
        ("Gold Necklace (22k)", 45000, "Traditional gold necklace design."),
        ("Diamond Ring", 35000, "Solitaire diamond ring in 18k gold."),
        ("Silver Anklets", 1500, "Sterling silver anklets pair."),
        ("Gold Earrings", 12000, "Stud earrings with intricate design."),
        ("Platinum Band", 25000, "Simple and elegant platinum band."),
        ("Pearl Necklace", 5000, "Freshwater pearl string necklace."),
        ("Gold Bangle", 30000, "Solid gold bangle for daily wear."),
        ("Nose Pin", 2000, "Gold nose pin with small diamond."),
        ("Silver Coin (10g)", 800, "999 purity silver coin."),
        ("Gemstone Pendant", 4000, "Ruby pendant with gold chain.")
    ],
    "Books & Stationery": [
        ("The Alchemist", 350, "Bestselling novel by Paulo Coelho."),
        ("Atomic Habits", 450, "Self-help book by James Clear."),
        ("Classmate Notebooks (Pack of 6)", 300, "Long notebooks for students."),
        ("Parker Pen", 500, "Classic stainless steel ball pen."),
        ("Harry Potter Box Set", 3500, "Complete collection of 7 books."),
        ("Scientific Calculator", 800, "Advanced calculator for engineering."),
        ("Art Sketchbook", 250, "A4 size sketchbook for artists."),
        ("Acrylic Paint Set", 450, "12 colors acrylic paint set."),
        ("Oxford Dictionary", 600, "Comprehensive English dictionary."),
        ("Sticky Notes", 100, "Colorful sticky notes for reminders.")
    ],
    "Footwear": [
        ("Formal Leather Shoes", 2500, "Black lace-up formal shoes."),
        ("Sports Sandals", 1200, "Comfortable sandals for daily use."),
        ("Canvas Sneakers", 999, "Casual white canvas shoes."),
        ("Running Slippers", 400, "Soft rubber slippers."),
        ("High Heels", 1800, "Party wear stilettos."),
        ("Hiking Boots", 3500, "Durable boots for trekking."),
        ("Loafers", 2200, "Slip-on casual loafers."),
        ("School Shoes", 800, "Black uniform shoes for kids."),
        ("Flip Flops", 300, "Beach wear flip flops."),
        ("Ethnic Mojaris", 1500, "Traditional embroidered footwear.")
    ]
}

def generate_random_coordinate_near_city(lat, lon, radius_km=10):
    # Rough approximation: 1 degree lat is ~111km
    offset = radius_km / 111.0
    new_lat = lat + random.uniform(-offset, offset)
    new_lon = lon + random.uniform(-offset, offset)
    return new_lat, new_lon

def generate_fake_data(db: Session, shops_count: int = 200, items_per_shop: int = 10):
    print(f"Starting massive fake data generation: Target {shops_count} shops...")
    
    generated_shops = []
    generated_items = []
    
    # Flatten city list to pick randomly
    all_cities: List[Dict[str, Any]] = []
    for state, cities in INDIA_DATA.items():
        for city_name, coords in cities.items():
            all_cities.append({"city": city_name, "state": state, "coords": coords})
            
    # Create a few vendor users to own these shops
    vendors = []
    for i in range(10): # Create 10 dummy vendors
        vendor_id = uuid.uuid4()
        vendor_email = f"vendor_bulk_{i}_{int(time.time())}@nearbuy.com"
        vendor_user = USER(
            id=vendor_id,
            email=vendor_email,
            password=security().hash_password("Vendor@123"),
            fullName=f"Vendor {i+1}",
            role=UserRole.VENDOR
        )
        # Check if exists first to avoid dupes if run multiple times
        existing = db.exec(select(USER).where(USER.email == vendor_email)).first()
        if not existing:
            db.add(vendor_user)
            vendors.append(vendor_user)
        else:
            vendors.append(existing)
    
    db.commit() # Commit vendors first
    
    shops_created = 0
    
    while shops_created < shops_count:
        # Pick a random city
        city_data = random.choice(all_cities)
        city_name = city_data["city"] 
        state_name = city_data["state"]
        base_lat, base_lon = city_data["coords"]
        
        # Pick a random category and shop name
        category = random.choice(list(SHOP_CATEGORIES.keys()))
        brand_name = random.choice(SHOP_CATEGORIES[category])
        
        # Unique shop name
        shop_name = f"{brand_name} {city_name} {random.randint(1, 999)}"
        
        # Random location near city center
        lat, lon = generate_random_coordinate_near_city(base_lat, base_lon)
        
        owner = random.choice(vendors)
        shop_id = uuid.uuid4()
        
        shop = SHOP(
            shop_id=shop_id,
            owner_id=owner.id,
            fullName=owner.fullName,
            shopName=shop_name,
            address=f"{random.randint(1, 100)}, {brand_name} Street, {city_name}, {state_name}",
            contact=f"+91-{random.randint(6000000000, 9999999999)}",
            description=f"Authorized {brand_name} store in {city_name}. Best deals on {category}.",
            is_open=True,
            latitude=lat,
            longitude=lon
        )
        db.add(shop)
        db.commit() # Commit shop to ensure ID exists for items
        generated_shops.append(shop)
        shops_created += 1
        
        # Generate items for this shop
        # Ensure we have items for this category
        category_items = ITEM_TEMPLATES.get(category, [])
        if not category_items:
            # Fallback
            category_items = ITEM_TEMPLATES["Grocery"]
            
        # Pick random items from the category
        # If items_per_shop is larger than available templates, we might duplicate with slight price diff
        for _ in range(items_per_shop):
            item_template = random.choice(category_items)
            name, base_price, desc = item_template
            
            # Vary price slightly
            price = base_price * random.uniform(0.9, 1.1)
            
            item = ITEM(
                id=uuid.uuid4(),
                shop_id=shop_id,
                itemName=name,
                price=round(price, 2),
                description=desc,
                note=f"Category: {category}"
            )
            db.add(item)
            generated_items.append(item)
            
        # Commit in batches of 50 shops to avoid massive transaction
        if shops_created % 50 == 0:
            print(f"  ...Created {shops_created} shops so far.")

    db.commit()
    print(f"Successfully generated {len(generated_shops)} shops and {len(generated_items)} items across India.")
    return len(generated_shops), len(generated_items)
