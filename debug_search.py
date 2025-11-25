#!/usr/bin/env python3
"""Debug script to check Typesense search functionality"""

from typesense_helper.typesense_client import get_typesense_client

def debug_search():
    ts_client = get_typesense_client()
    
    # Check collections
    print("=== Collection Stats ===")
    shops_stats = ts_client.collections['shops'].retrieve()
    items_stats = ts_client.collections['items'].retrieve()
    print(f"Shops collection: {shops_stats['num_documents']} documents")
    print(f"Items collection: {items_stats['num_documents']} documents")
    
    # Search for rice items
    print("\n=== Searching for 'rice' items ===")
    item_search_params = {
        'q': 'rice',
        'query_by': 'itemName,description',
        'per_page': 10
    }
    item_results = ts_client.collections['items'].documents.search(item_search_params)
    print(f"Found {len(item_results['hits'])} items matching 'rice'")
    
    if item_results['hits']:
        print("\nFirst few results:")
        for i, hit in enumerate(item_results['hits'][:3]):
            doc = hit['document']
            print(f"{i+1}. Item: {doc.get('itemName')} | Shop ID: {doc.get('shop_id')}")
    
        # Get shop IDs
        shop_ids = {hit['document']['shop_id'] for hit in item_results['hits']}
        print(f"\nUnique shop IDs with rice: {len(shop_ids)}")
        
        # Search for shops in Agartala area
        lat, lon = 23.8315, 91.2868
        radius_km = 5
        radius_km_str = f"{radius_km} km"
        
        print(f"\n=== Searching shops near Agartala ({lat}, {lon}) within {radius_km}km ===")
        shop_search_params = {
            'q': '*',
            'filter_by': f'shop_id:[{",".join(shop_ids)}] && location:({lat}, {lon}, {radius_km_str})',
            'sort_by': f'location({lat}, {lon}):asc',
            'per_page': 50
        }
        print(f"Filter: {shop_search_params['filter_by']}")
        
        try:
            shop_results = ts_client.collections['shops'].documents.search(shop_search_params)
            print(f"Found {len(shop_results['hits'])} shops")
            
            if shop_results['hits']:
                print("\nShops found:")
                for hit in shop_results['hits']:
                    doc = hit['document']
                    dist_m = hit.get('geo_distance_meters', {}).get('location', 0)
                    dist_km = dist_m / 1000
                    print(f"  - {doc['shopName']} ({dist_km:.2f} km away)")
            else:
                print("\nNo shops found in this area with rice items.")
                
                # Try searching all shops in the area (no filter)
                print(f"\n=== Searching ALL shops near Agartala ===")
                all_shops_params = {
                    'q': '*',
                    'filter_by': f'location:({lat}, {lon}, {radius_km_str})',
                    'sort_by': f'location({lat}, {lon}):asc',
                    'per_page': 10
                }
                all_shops = ts_client.collections['shops'].documents.search(all_shops_params)
                print(f"Found {len(all_shops['hits'])} shops total in area")
                
                if all_shops['hits']:
                    print("\nShops in area:")
                    for hit in all_shops['hits']:
                        doc = hit['document']
                        dist_m = hit.get('geo_distance_meters', {}).get('location', 0)
                        dist_km = dist_m / 1000
                        print(f"  - {doc['shopName']} | ID: {doc['shop_id']} ({dist_km:.2f} km)")
                        
        except Exception as e:
            print(f"Error searching shops: {e}")
            import traceback
            traceback.print_exc()
    
if __name__ == "__main__":
    debug_search()
