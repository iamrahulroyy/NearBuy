import traceback
import typesense
from app.helpers.variables import TYPESENSE_HOST, TYPESENSE_PORT, TYPESENSE_PROTOCOL, TYPESENSE_API_KEY

client = typesense.Client({
    'nodes': [{
        'host': TYPESENSE_HOST,
        'port': TYPESENSE_PORT,
        'protocol': TYPESENSE_PROTOCOL
    }],
    'api_key': TYPESENSE_API_KEY,
    'connection_timeout_seconds': 5
})

shops_schema = {
    "name": "shops",
    "fields": [
        {"name": "shop_id", "type": "string"},
        {"name": "owner_id", "type": "string", "facet": True},
        {"name": "shopName", "type": "string"},
        {"name": "fullName", "type": "string"},
        {"name": "address", "type": "string"},
        {"name": "description", "type": "string", "optional": True},
        {"name": "location", "type": "geopoint"},
    ],
}

items_schema = {
    "name": "items",
    "fields": [
        # Changed "id" to "item_id" to avoid conflict with Typesense's reserved "id" field
        {"name": "item_id", "type": "string"},
        {"name": "shop_id", "type": "string", "facet": True},
        {"name": "itemName", "type": "string"},
        {"name": "description", "type": "string", "optional": True},
        {"name": "price", "type": "float"},
        {"name": "note", "type": "string", "optional": True},
    ],
}

def create_collections():
    # DROP and RECREATE shops collection to enforce correct geopoint type
    try:
        client.collections['shops'].delete()
    except typesense.exceptions.ObjectNotFound:
        pass
    client.collections.create(shops_schema)

    try:
        client.collections['items'].retrieve()
    except typesense.exceptions.ObjectNotFound:
        client.collections.create(items_schema)


def get_typesense_client():
    return client