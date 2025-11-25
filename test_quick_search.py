#!/usr/bin/env python3
"""Test all quick-search items in Agartala"""

from typesense_helper.typesense_client import get_typesense_client

def test_quick_search_items():
    ts_client = get_typesense_client()
    
    # Quick search items to test
    quick_search_items = [
        "Batteries",
        "Milk",
        "Chargers",
        "Rice",
        "Headphones",
        "Cooking Oil",
        "Dumbbells",
        "Football",
        "Bookshelf"
    ]
    
    # Test location: Agartala
    lat, lon = 23.8315, 91.2868
    radius_km = 10
    
    print(f"Testing Quick Search Items in Agartala (radius: {radius_km}km)")
    print("=" * 70)
    
    for item_query in quick_search_items:
        # Search for item
        item_search_params = {
            'q': item_query,
            'query_by': 'itemName,description',
            'per_page': 250
        }
        item_results = ts_client.collections['items'].documents.search(item_search_params)
        
        if not item_results['hits']:
            print(f"❌ {item_query:20s} - No items found in database")
            continue
        
        shop_ids = {hit['document']['shop_id'] for hit in item_results['hits']}
        
        # Search for nearby shops
        radius_km_str = f"{radius_km} km"
        shop_search_params = {
            'q': '*',
            'filter_by': f'shop_id:[{",".join(shop_ids)}] && location:({lat}, {lon}, {radius_km_str})',
            'sort_by': f'location({lat}, {lon}):asc',
            'per_page': 10
        }
        
        shop_results = ts_client.collections['shops'].documents.search(shop_search_params)
        
        if shop_results['hits']:
            shop = shop_results['hits'][0]['document']
            dist_m = shop_results['hits'][0].get('geo_distance_meters', {}).get('location', 0)
            dist_km = dist_m / 1000
            print(f"✅ {item_query:20s} - Found at {shop['shopName']} ({dist_km:.2f} km)")
        else:
            print(f"⚠️  {item_query:20s} - Item exists globally ({len(item_results['hits'])} items) but none in Agartala area")

if __name__ == "__main__":
    test_quick_search_items()
