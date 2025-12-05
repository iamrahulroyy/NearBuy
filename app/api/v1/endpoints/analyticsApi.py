"""
Analytics API endpoint - Real-time statistics
"""

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func
from typing import Dict

from app.db.session import DataBasePool
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.models.user import USER, UserRole

router = APIRouter()


@router.get("/stats", response_model=Dict)
async def get_platform_stats() -> Dict:
    """
    Get real-time platform statistics

    Returns:
        - cities_count: Number of unique cities with shops
        - shops_count: Total number of shops
        - users_count: Total number of users
        - items_count: Total number of items
        - vendors_count: Total number of vendors
    """
    try:
        # Get database session
        db = DataBasePool._db_pool
        if db is None:
            raise HTTPException(status_code=500, detail="Database not available")

        # Count unique cities from shop addresses
        # We'll count distinct unique locations based on lat/lon pairs
        cities_count_query = select(func.count(func.distinct(SHOP.address)))
        cities_result = db.exec(cities_count_query).one()

        # More accurate: count distinct city names from addresses
        # Extract city from address (this is approximate)
        shops = db.exec(select(SHOP)).all()
        cities = set()
        for shop in shops:
            if shop.address:
                # Try to extract city from address
                # Typically format is: "..., City, State PIN"
                parts = [p.strip() for p in shop.address.split(",")]
                if len(parts) >= 2:
                    # Second-to-last part is usually the city
                    city = parts[-2] if len(parts) > 2 else parts[-1]
                    # Remove PIN codes
                    city = " ".join(
                        [word for word in city.split() if not word.isdigit()]
                    )
                    cities.add(city.strip())

        cities_count = len(cities) if cities else cities_result or 0

        # Count shops
        shops_query = select(func.count()).select_from(SHOP)
        shops_count = db.exec(shops_query).one() or 0

        # Count total users
        users_query = select(func.count()).select_from(USER)
        users_count = db.exec(users_query).one() or 0

        # Count items
        items_query = select(func.count()).select_from(ITEM)
        items_count = db.exec(items_query).one() or 0

        # Count vendors specifically
        vendors_query = (
            select(func.count()).select_from(USER).where(USER.role == UserRole.VENDOR)
        )
        vendors_count = db.exec(vendors_query).one() or 0

        return {
            "cities_count": cities_count,
            "shops_count": shops_count,
            "users_count": users_count,
            "items_count": items_count,
            "vendors_count": vendors_count,
            "success": True,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching statistics: {str(e)}"
        )
