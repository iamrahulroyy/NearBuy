import os
import sys
from sqlmodel import Session, create_engine, select
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from typesense_helper.typesense_client import get_typesense_client, create_collections
from app.helpers.variables import DATABASE_URL

engine = create_engine(DATABASE_URL)

def sync_database_to_typesense():
    ts_client = get_typesense_client()
    print("Ensuring Typesense collections exist...")
    create_collections()

    with Session(engine) as session:
        print("Fetching all shops from the database...")
        shops = session.exec(select(SHOP)).all()
        print(f"Found {len(shops)} shops in database")
        
        shop_documents = []
        for shop in shops:
            print(f"Processing shop: {shop.shop_id}")
            
            # Use latitude and longitude directly from the model
            if shop.latitude is not None and shop.longitude is not None:
                shop_doc = {
                    "shop_id": str(shop.shop_id),
                    "owner_id": str(shop.owner_id),
                    "shopName": shop.shopName,
                    "fullName": shop.fullName,
                    "address": shop.address,
                    "contact": shop.contact if shop.contact else "",
                    "description": shop.description if shop.description else "",
                    "is_open": shop.is_open,
                    "location": [shop.latitude, shop.longitude],
                }
                shop_documents.append(shop_doc)
                print(f"Added shop: {shop.shopName} at ({shop.latitude}, {shop.longitude})")
            else:
                print(f"Skipping shop {shop.shop_id} - no valid coordinates")

        print(f"Total shop documents to index: {len(shop_documents)}")
        
        if shop_documents:
            print(f"Indexing {len(shop_documents)} shops...")
            result = ts_client.collections["shops"].documents.import_(
                shop_documents, {"action": "upsert"}
            )
            print(f"Import result: {result}")
            print("Finished indexing shops.")
        else:
            print("No shop documents to index!")
            
        print("Fetching all items from the database...")
        items = session.exec(select(ITEM)).all()
        print(f"Found {len(items)} items in database")
        item_documents = []
        for item in items:
            item_documents.append({
                "item_id": str(item.id),  # Changed from "id" to "item_id" to match schema
                "itemName": item.itemName,
                "description": item.description if item.description else "",
                "shop_id": str(item.shop_id),
                "price": item.price,
                "note": item.note if item.note else "",
            })

        if item_documents:
            print(f"Indexing {len(item_documents)} items...")
            result = ts_client.collections["items"].documents.import_(
                item_documents, {"action": "upsert"}
            )
            print(f"Import result summary: {len([r for r in result if r.get('success')])} successful")
            print("Finished indexing items.")

if __name__ == "__main__":
    print("Starting full database sync to Typesense...")
    sync_database_to_typesense()
    print("Sync complete.")
