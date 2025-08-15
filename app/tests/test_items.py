import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock, MagicMock

from main import app
from app.db.models.user import USER, USER_SESSION, UserRole
from app.db.models.shop import SHOP
from app.db.models.item import ITEM
from app.db.session import DataBasePool

# --- Test Constants ---
TEST_OWNER_ID = uuid.UUID("3e592b3b-5064-4ff5-9fcf-2bf8382972fe")
TEST_SHOP_ID = "07446c46-7775-4c99-a29e-79843fb69f93"
TEST_ITEM_NAME = f"Definitive-Widget-{uuid.uuid4()}"
TEST_ITEM_ID = uuid.uuid4()

# --- Mock Data ---
mock_user_session = USER_SESSION(
    pk="test_session_token", email="testvendor@example.com", role=UserRole.VENDOR,
    ip="127.0.0.1", browser="test-client", os="pytest",
    created_at=1672531200, expired_at=9999999999
)
mock_db_user = USER(id=TEST_OWNER_ID, email="testvendor@example.com", role=UserRole.VENDOR)
mock_shop = SHOP(shop_id=uuid.UUID(TEST_SHOP_ID), owner_id=TEST_OWNER_ID, shopName="Test Shop")

# --- Pytest Fixture ---
@pytest_asyncio.fixture
async def client():
    await DataBasePool.setup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    await DataBasePool.teardown()

# --- Item API Tests ---
@pytest.mark.asyncio
async def test_add_item(client: AsyncClient):
    """Test successfully adding a new item."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.items.DB.get_attr_all") as mock_get_attr:
        mock_get_attr.side_effect = [mock_shop, mock_db_user, None] # Shop owner check
        item_data = {"shop_id": TEST_SHOP_ID, "itemName": TEST_ITEM_NAME, "price": 19.99}
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.post("/items/add_item", json=item_data, headers=headers)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_item(client: AsyncClient):
    """Test retrieving a specific item by name."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get(f"/items/get_item/{TEST_ITEM_NAME}", headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_all_items(client: AsyncClient):
    """Test retrieving a paginated list of all items."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get("/items/get_all_items", headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    """Test successfully updating an existing item."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.items.DB.get_attr_all") as mock_get_attr, \
         patch("app.api.v1.endpoints.functions.items.DB.update_attr_all", new_callable=AsyncMock) as mock_update:
        
        # DEFINITIVE FIX: Mock the DB calls specifically for the update endpoint's logic.
        mock_existing_item = ITEM(id=TEST_ITEM_ID, itemName=TEST_ITEM_NAME, price=19.99, shop_id=uuid.UUID(TEST_SHOP_ID))
        mock_updated_item = ITEM(id=TEST_ITEM_ID, itemName=TEST_ITEM_NAME, price=25.50, shop_id=uuid.UUID(TEST_SHOP_ID))
        
        # The endpoint calls get_attr_all TWICE: once to find the item, and once to return the updated version.
        mock_get_attr.side_effect = [mock_existing_item, mock_updated_item]
        mock_update.return_value = ("Updated successfully", True)

        update_data = {"shop_id": TEST_SHOP_ID, "itemName": TEST_ITEM_NAME, "price": 25.50}
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.patch("/items/update_item", json=update_data, headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] == "Item updated successfully"
    assert response_body["body"]["price"] == 25.50

@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    """Test successfully deleting an item."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.delete(f"/items/delete_item?itemName={TEST_ITEM_NAME}", headers=headers)
    assert response.status_code == 200