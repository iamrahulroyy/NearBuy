from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session, select, func, create_engine
from app.db.models.shop import SHOP
from typing import Optional, TypedDict
from app.helpers.variables import DATABASE_URL

engine = create_engine(DATABASE_URL)

limiter = Limiter(key_func=get_remote_address)
categories_router = APIRouter()

# Predefined categories with icon emojis
CATEGORY_MAP = {
    "electronics": {"name": "Electronics", "icon": "📱"},
    "grocery": {"name": "Grocery & Food", "icon": "🛒"},
    "fashion": {"name": "Fashion & Apparel", "icon": "👕"},
    "health": {"name": "Health & Beauty", "icon": "💊"},
    "sports": {"name": "Sports & Fitness", "icon": "⚽"},
    "books": {"name": "Books & Stationery", "icon": "📚"},
    "home": {"name": "Home & Living", "icon": "🏠"},
    "toys": {"name": "Toys & Games", "icon": "🎮"},
}

class CategoryDict(TypedDict):
    id: str
    name: str
    icon: str
    count: int

def categorize_shop(shop_name: str, description: str = "") -> str:
    """Categorize shop based on name and description"""
    text = f"{shop_name} {description}".lower()
    
    if any(word in text for word in ["gadget", "gear", "electronic", "phone", "laptop", "tech"]):
        return "electronics"
    elif any(word in text for word in ["fresh", "grocery", "food", "daily", "milk", "bread"]):
        return "grocery"
    elif any(word in text for word in ["fashion", "thread", "cloth", "apparel", "dress"]):
        return "fashion"
    elif any(word in text for word in ["health", "beauty", "cosmetic", "salon", "spa"]):
        return "health"
    elif any(word in text for word in ["sport", "fitness", "active", "gym"]):
        return "sports"
    elif any(word in text for word in ["book", "reader", "paradise", "library", "stationery"]):
        return "books"
    elif any(word in text for word in ["home", "furniture", "comfort", "living"]):
        return "home"
    elif any(word in text for word in ["toy", "game", "kids", "play"]):
        return "toys"
    else:
        return "grocery"  # Default category

@categories_router.get("", description="Get all available categories with shop counts")
@limiter.limit("30/minute")
def get_categories(request: Request):
    try:
        # Get all shops
        with Session(engine) as session:
            shops = session.exec(select(SHOP)).all()
        
        # Count shops by category
        category_counts: dict[str, int] = {}
        for shop in shops:
            category = categorize_shop(shop.shopName, shop.description or "")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Build response
        categories: list[CategoryDict] = []
        for cat_id, info in CATEGORY_MAP.items():
            count = category_counts.get(cat_id, 0)
            if count > 0:  # Only include categories with shops
                categories.append({
                    "id": cat_id,
                    "name": info["name"],
                    "icon": info["icon"],
                    "count": count
                })
        
        # Sort by count (descending)
        categories.sort(key=lambda x: x["count"], reverse=True)
        
        return {
            "status": 200,
            "message": "Categories retrieved successfully",
            "categories": categories
        }
        
    except Exception as e:
        print(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")
