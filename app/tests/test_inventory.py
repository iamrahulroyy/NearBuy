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
TEST_OWNER_ID = uuid.UUID("3e5b2b3b-5064-4ff5-9fcf-2bf8382972fe")
TEST_SHOP_ID = "07446c46-7775-4c99-a29e-79843fb69f93"
TEST_ITEM_ID = "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"
TEST_INVENTORY_ID = "inv-abc-123-xyz-789"

# --- Mock Data ---
mock_user_session = USER_SESSION(
    pk="test_session_token", email="testvendor@example.com", role=UserRole.VENDOR,
    ip="127.0.0.1", browser="test-client", os="pytest",
    created_at=1672531200, expired_at=9999999999
)
mock_db_user = USER(id=TEST_OWNER_ID, email="testvendor@example.com", role=UserRole.VENDOR)
mock_shop = SHOP(shop_id=uuid.UUID(TEST_SHOP_ID), owner_id=TEST_OWNER_ID, shopName="Test Shop")
mock_item = ITEM(id=uuid.UUID(TEST_ITEM_ID), shop_id=uuid.UUID(TEST_SHOP_ID), itemName="Testable Widget")


@pytest_asyncio.fixture
async def client():
    await DataBasePool.setup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    await DataBasePool.teardown()

# --- Inventory API Tests ---

@pytest.mark.asyncio
async def test_add_inventory(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.inventory.db.get_attr_all") as mock_get_attr, \
         patch("app.api.v1.endpoints.functions.inventory.db.insert", new_callable=AsyncMock) as mock_insert, \
         patch("uuid.uuid4", return_value=TEST_INVENTORY_ID):

        mock_get_attr.side_effect = [
            mock_shop, mock_db_user, mock_item, None
        ]
        mock_insert.return_value = (MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}}), True)

        inventory_data = {
            "shop_id": TEST_SHOP_ID,
            "item_id": TEST_ITEM_ID,
            "quantity": 100,
            "min_quantity": 10,
            "max_quantity": 200
        }
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.post("/inventory/add", json=inventory_data, headers=headers)

    assert response.status_code == 201
    assert response.json()["message"] == "Inventory added"


@pytest.mark.asyncio
async def test_update_inventory(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.inventory.db.get_attr_all") as mock_get_attr, \
         patch("app.api.v1.endpoints.functions.inventory.db.update_attr_all", new_callable=AsyncMock) as mock_update:

        mock_inventory_record = MagicMock(
            shop_id=TEST_SHOP_ID, 
            quantity=100,  
            spec=["model_dump"], 
            **{"model_dump.return_value": {}}
        )
        mock_updated_record = MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}})

        mock_get_attr.side_effect = [
            mock_inventory_record, mock_shop, mock_db_user, mock_updated_record
        ]
        mock_update.return_value = ("Updated successfully.", True)

        update_data = {
            "inventory_id": TEST_INVENTORY_ID,
            "quantity": 95 
        }
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.patch("/inventory/update", json=update_data, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Inventory updated"


@pytest.mark.asyncio
async def test_get_inventory_by_id(client: AsyncClient):
    """Test retrieving a specific inventory record by its ID."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.inventory.db.get_attr_all") as mock_get_attr:
        
        mock_get_attr.return_value = MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}})

        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get(f"/inventory/{TEST_INVENTORY_ID}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Inventory found"


@pytest.mark.asyncio
async def test_get_inventory_for_shop(client: AsyncClient):
    """Test retrieving all inventory records for a given shop."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.inventory.db.get_attr_all") as mock_get_attr:

        mock_get_attr.return_value = [
            MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}}), 
            MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}})
        ]

        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get(f"/inventory/shop/{TEST_SHOP_ID}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Inventories found"
    assert len(response.json()["body"]) == 2


@pytest.mark.asyncio
async def test_delete_inventory(client: AsyncClient):
    """Test successfully deleting an inventory record."""
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.inventory.db.get_attr_all") as mock_get_attr, \
         patch("app.api.v1.endpoints.functions.inventory.db.delete_attr", new_callable=AsyncMock) as mock_delete:
        
        mock_get_attr.return_value = MagicMock(spec=["model_dump"], **{"model_dump.return_value": {}})
        mock_delete.return_value = ("Deleted successfully.", True)

        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.delete(f"/inventory/{TEST_INVENTORY_ID}", headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Inventory deleted"