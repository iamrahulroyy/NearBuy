from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.helpers.helpers import send_json_response
import traceback

class SearchDB:

    async def search_shops(self, request, q: str, db_pool):
        try:
            # SQLModel uses select + where - for ILIKE, use .ilike() of column with the search pattern
            stmt = select(SHOP).where(SHOP.shopName.ilike(f"%{q}%"))
            result = db_pool.exec(stmt).scalars().all()  # scalars() returns model instances

            shops = [shop.model_dump(mode='json', exclude={'location'}) for shop in result]

            return send_json_response(message="Shop search results", status=200, body=shops)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error searching shops", status=500, body=[])

    async def search_items(self, request, q: str, db_pool):
        try:
            stmt = select(ITEM).where((ITEM.itemName.ilike(f"%{q}%")) |(ITEM.description.ilike(f"%{q}%")))
            result = db_pool.exec(stmt).scalars().all()

            items = [item.model_dump(mode='json') for item in result]

            return send_json_response(message="Item search results", status=200, body=items)
        except Exception as e:
            traceback.print_exc()
            return send_json_response(message="Error searching items", status=500, body=[])
