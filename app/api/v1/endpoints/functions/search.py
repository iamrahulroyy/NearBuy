from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import typesense
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.helpers.helpers import send_json_response
import traceback

class SearchDB:

    # async def search_shops(self, request, q: str, db_pool):
    #     try:
    #         # SQLModel uses select + where - for ILIKE, use .ilike() of column with the search pattern
    #         stmt = select(SHOP).where(SHOP.shopName.ilike(f"%{q}%"))
    #         result = db_pool.exec(stmt).scalars().all()  # scalars() returns model instances

    #         shops = [shop.model_dump(mode='json', exclude={'location'}) for shop in result]

    #         return send_json_response(message="Shop search results", status=200, body=shops)
    #     except Exception as e:
    #         traceback.print_exc()
    #         return send_json_response(message="Error searching shops", status=500, body=[])

    # async def search_items(self, request, q: str, db_pool):
    #     try:
    #         stmt = select(ITEM).where((ITEM.itemName.ilike(f"%{q}%")) |(ITEM.description.ilike(f"%{q}%")))
    #         result = db_pool.exec(stmt).scalars().all()

    #         items = [item.model_dump(mode='json') for item in result]

    #         return send_json_response(message="Item search results", status=200, body=items)
    #     except Exception as e:
    #         traceback.print_exc()
    #         return send_json_response(message="Error searching items", status=500, body=[])

    def search_nearby_items(self, q: str, lat: float, lon: float, radius_km: int, ts_client: typesense.Client):
        try:
            # Debug: Check if collections exist and have documents
            shops_stats = ts_client.collections['shops'].retrieve()
            items_stats = ts_client.collections['items'].retrieve()
            # print(f"Shops collection: {shops_stats['num_documents']} documents")
            # print(f"Items collection: {items_stats['num_documents']} documents")
            
            if shops_stats['num_documents'] == 0:
                return send_json_response(
                    message="No shops are currently indexed. Please sync the database first.", 
                    status=200, 
                    body=[]
                )
            
            radius_km_str = f"{radius_km} km"

            item_search_params = {
                'q': q,
                'query_by': 'itemName,description',
                'per_page': 250
            }
            
            # print(f"Searching items with params: {item_search_params}")
            item_results = ts_client.collections['items'].documents.search(item_search_params)
            # print(f"Item search returned {len(item_results['hits'])} results")

            if not item_results['hits']:
                return send_json_response(message="No items found matching your query.", status=200, body=[])

            shop_ids = {hit['document']['shop_id'] for hit in item_results['hits']}
            # print(f"Found shop IDs: {shop_ids}")
            
            if not shop_ids:
                return send_json_response(message="Items were found, but they are not associated with any shops.", status=200, body=[])

            shop_search_params = {
                'q': '*',
                'filter_by': f'shop_id:[{",".join(shop_ids)}] && location:({lat}, {lon}, {radius_km_str})',
                'sort_by': f'location({lat}, {lon}):asc', 
                'per_page': 50
            }
            
            # print(f"Searching shops with params: {shop_search_params}")
            shop_results = ts_client.collections['shops'].documents.search(shop_search_params)
            # print(f"Shop search returned {len(shop_results['hits'])} results")

            return send_json_response(message="Nearby shops with the item found.", status=200, body=shop_results['hits'])

        except typesense.exceptions.RequestMalformed as e:
            print(f"RequestMalformed error: {e}")
            raise HTTPException(status_code=400, detail=f"Search query is malformed: {e}")
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="An internal error occurred during the search.")