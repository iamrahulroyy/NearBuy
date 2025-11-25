from fastapi import APIRouter, HTTPException, Depends, Request, Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlmodel import Session, select, create_engine
from app.db.models.shop import SHOP
from typing import Optional
from app.helpers.variables import DATABASE_URL

engine = create_engine(DATABASE_URL)
limiter = Limiter(key_func=get_remote_address)
shops_list_router = APIRouter()

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
        return "grocery"

def extract_city(address: str) -> str:
    """Extract city from address"""
    parts = address.split(",")
    if len(parts) >= 2:
        return parts[1].strip()
    return "Unknown"

@shops_list_router.get("", description="Get all shops with optional filters")
@limiter.limit("30/minute")
def get_shops_list(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    city: Optional[str] = Query(None, description="Filter by city"),
    is_open: Optional[bool] = Query(None, description="Filter by open status"),
    limit: int = Query(50, ge=1, le=100, description="Number of shops to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    try:
        with Session(engine) as session:
            query = select(SHOP)
            all_shops = session.exec(query).all()
        
        filtered_shops = []
        for shop in all_shops:
            if category:
                shop_category = categorize_shop(shop.shopName, shop.description or "")
                if shop_category != category:
                    continue
            
            if city:
                shop_city = extract_city(shop.address)
                if shop_city.lower() != city.lower():
                    continue
            
            if is_open is not None and shop.is_open != is_open:
                continue
            
            filtered_shops.append(shop)
        
        total = len(filtered_shops)
        paginated_shops = filtered_shops[offset:offset + limit]
        
        shops_data = []
        for shop in paginated_shops:
            shops_data.append({
                "shop_id": str(shop.shop_id),
                "shopName": shop.shopName,
                "fullName": shop.fullName,
                "address": shop.address,
                "contact": shop.contact,
                "description": shop.description,
                "is_open": shop.is_open,
                "latitude": shop.latitude,
                "longitude": shop.longitude,
                "category": categorize_shop(shop.shopName, shop.description or ""),
                "city": extract_city(shop.address)
            })
        
        return {
            "status": 200,
            "message": f"Found {total} shops",
            "total": total,
            "limit": limit,
            "offset": offset,
            "shops": shops_data
        }
        
    except Exception as e:
        print(f"Error fetching shops: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch shops")
