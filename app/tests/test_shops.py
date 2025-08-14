import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.api.v1.endpoints.functions.shops import SDB
from app.db.models.shop import SHOP

@pytest.mark.asyncio
async def test_get_shop_cache_miss():
    shop_instance = SHOP(
        shop_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
        owner_id="owner-uuid-123",
        shopName="Test Coffee Shop",
        fullName="John Doe",
        address="123 Test St",
        location=None
    )

    mock_db = MagicMock()
    mock_db.get_attr_all = AsyncMock(return_value=shop_instance)

    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True

    mock_request = MagicMock()

    response = await SDB.get_shop(
        request=mock_request,
        shop_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
        db_pool=mock_db,
        redis_client=mock_redis
    )

    assert response.status_code == 200
    response_body = json.loads(response.body)
    assert response_body["message"] == "Shop retrieved from database"
    assert response_body["body"]["shop_id"] == "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    assert response_body["body"]["shopName"] == "Test Coffee Shop"


@pytest.mark.asyncio
async def test_get_shop_cache_hit():
    fake_cached_shop = {
        "shop_id": "cached-id-123",
        "shopName": "Cached Coffee Shop",
        "owner_id": "owner-uuid-456",
        "fullName": "Jane Doe",
        "address": "456 Cache Ave",
        "location": None
    }

    mock_db = MagicMock()
    mock_db.get_attr_all = AsyncMock()

    mock_redis = MagicMock()
    mock_redis.get.return_value = json.dumps(fake_cached_shop)
    mock_redis.set.return_value = True

    mock_request = MagicMock()

    response = await SDB.get_shop(
        request=mock_request,
        shop_id="cached-id-123",
        db_pool=mock_db,
        redis_client=mock_redis
    )

    assert response.status_code == 200
    response_body = json.loads(response.body)
    assert response_body["message"] == "Shop retrieved from cache"
    assert response_body["body"]["shop_id"] == "cached-id-123"
    assert response_body["body"]["shopName"] == "Cached Coffee Shop"
