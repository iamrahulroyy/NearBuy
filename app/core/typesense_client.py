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
    'connection_timeout_seconds': 2
})

shops_schema = {
    'name': 'shops',
    'fields': [
        {'name': 'shop_id', 'type': 'string'},
        {'name': 'owner_id', 'type': 'string', 'facet': True},
        {'name': 'fullName', 'type': 'string'},
        {'name': 'shopName', 'type': 'string'},
        {'name': 'address', 'type': 'string'},
        {'name': 'contact', 'type': 'string', 'optional': True},
        {'name': 'description', 'type': 'string', 'optional': True},
        {'name': 'is_open', 'type': 'bool'},
        {'name': 'location', 'type': 'geopoint', 'optional': True},
        {'name': 'created_at', 'type': 'int32'},
        {'name': 'updated_at', 'type': 'int32', 'optional': True},
        {'name': 'note', 'type': 'string', 'optional': True}
    ],
    'default_sorting_field': 'created_at'
}


items_schema = {
    'name': 'items',
    'fields': [
        {'name': 'id', 'type': 'string'},  
        {'name': 'itemName', 'type': 'string'},
        {'name': 'price', 'type': 'float'},
        {'name': 'description', 'type': 'string', 'optional': True},
        {'name': 'note', 'type': 'string', 'optional': True}
    ],
    'default_sorting_field': 'price'
}


def create_collections():
    try:
        client.collections['shops'].retrieve()
    except typesense.exceptions.ObjectNotFound:
        client.collections.create(shops_schema)

    try:
        client.collections['items'].retrieve()
    except typesense.exceptions.ObjectNotFound:
        client.collections.create(items_schema)

def get_typesense_client():
    return client
