#!/usr/bin/env python3
"""Reset Typesense collections and sync fresh data from database"""

from typesense_helper.typesense_client import get_typesense_client, create_collections

def reset_collections():
    ts_client = get_typesense_client()
    
    # Delete existing collections
    print("Deleting existing collections...")
    try:
        ts_client.collections['shops'].delete()
        print("  - Deleted 'shops' collection")
    except Exception as e:
        print(f"  - Could not delete 'shops': {e}")
    
    try:
        ts_client.collections['items'].delete()
        print("  - Deleted 'items' collection")
    except Exception as e:
        print(f"  - Could not delete 'items': {e}")
    
    # Recreate collections
    print("\nRecreating collections...")
    create_collections()
    print("  - Collections recreated successfully")
    
    # Now sync the data
    print("\nSyncing data from database...")
    from typesense_helper.sync_db_to_typesense import sync_database_to_typesense
    sync_database_to_typesense()

if __name__ == "__main__":
    reset_collections()
    print("\n=== Reset and sync complete! ===")
