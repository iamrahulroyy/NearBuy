#!/usr/bin/env python3
"""Test search in different cities to verify it's working"""

from typesense_helper.typesense_client import get_typesense_client

def test_search_in_cities():
    ts_client = get_typesense_client()
    
    test_cities = [
        ("Agartala", 23.8315, 91.2868, 20),  # Larger radius
        ("Guwahati", 26.1445, 91.7362, 10),
        ("Kolkata", 22.5726, 88.3639, 10),
    ]
    
    for city, lat, lon, radius_km in test_cities:
        print(f"\n{'='*60}")
        print(f"Testing {city} ({lat}, {lon}) within {radius_km}km")
        print('='*60)
        
        # Search for rice items
        item_search_params = {
            'q': 'rice',
            'query_by': 'itemName,description',
            'per_page': 250
        }
        item_results = ts_client.collections['items'].documents.search(item_search_params)
        shop_ids = {hit['document']['shop_id'] for hit in item_results['hits']}
        
        # Search for shops in area
        radius_km_str = f"{radius_km} km"
        shop_search_params = {
            'q': '*',
            'filter_by': f'shop_id:[{",".join(shop_ids)}] && location:({lat}, {lon}, {radius_km_str})',
            'sort_by': f'location({lat}, {lon}):asc',
            'per_page': 50
        }
        
        try:
            shop_results = ts_client.collections['shops'].documents.search(shop_search_params)
            print(f"✅ Found {len(shop_results['hits'])} shops with rice")
            
            if shop_results['hits']:
                for i, hit in enumerate(shop_results['hits'][:3], 1):
                    doc = hit['document']
                    dist_m = hit.get('geo_distance_meters', {}).get('location', 0)
                    dist_km = dist_m / 1000
                    print(f"  {i}. {doc['shopName']} ({dist_km:.2f} km)")
                    
                if len(shop_results['hits']) > 3:
                    print(f"  ... and {len(shop_results['hits']) - 3} more")
            else:
                print("  ❌ No rice found in this area")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_search_in_cities()
