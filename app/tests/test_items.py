import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from main import app
from app.db.models.user import USER, USER_SESSION, UserRole
from app.db.models.shop import SHOP
from app.db.session import DataBasePool


TEST_OWNER_ID = uuid.UUID("3e592b3b-5064-4ff5-9fcf-2bf8382972fe")
TEST_SHOP_ID = "07446c46-7775-4c99-a29e-79843fb69f93"
TEST_ITEM_NAME = f"Testable Super-Widget {uuid.uuid4()}"

mock_user_session = USER_SESSION(
    pk="test_session_token", email="testvendor@example.com", role=UserRole.VENDOR,
    ip="127.0.0.1", browser="test-client", os="pytest",
    created_at=1672531200, expired_at=9999999999
)


mock_db_user = USER(id=TEST_OWNER_ID, email="testvendor@example.com", role=UserRole.VENDOR)


mock_shop = SHOP(shop_id=uuid.UUID(TEST_SHOP_ID), owner_id=TEST_OWNER_ID, shopName="Test Shop")



@pytest_asyncio.fixture
async def client():
    await DataBasePool.setup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    await DataBasePool.teardown()


# --- Item API Tests ---
@pytest.mark.asyncio
async def test_add_item(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session), \
         patch("app.api.v1.endpoints.functions.items.DB.get_attr_all") as mock_get_attr:

        mock_get_attr.side_effect = [
            mock_shop,      
            mock_db_user,   
            None           
        ]

        item_data = {
            "shop_id": TEST_SHOP_ID, "itemName": TEST_ITEM_NAME, "price": 19.99,
            "description": "A high-quality widget for testing.", "note": "Handle with care"
        }
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.post("/items/add_item", json=item_data, headers=headers)

    assert response.status_code == 201
    response_body = response.json()
    assert response_body["message"] == "Item added successfully"
    assert response_body["body"]["itemName"] == TEST_ITEM_NAME


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        await test_add_item(client)
        response = await client.get(f"/items/get_item/{TEST_ITEM_NAME}", headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] in ["Item retrieved successfully", "Item retrieved from cache"]
    assert response_body["body"]["itemName"] == TEST_ITEM_NAME


@pytest.mark.asyncio
async def test_get_all_items(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get("/items/get_all_items", headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] in ["Items retrieved successfully", "Items retrieved from cache"]
    assert len(response_body["body"]["data"]) > 0


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        await test_add_item(client)
        
        update_data = {
            "shop_id": TEST_SHOP_ID, "itemName": TEST_ITEM_NAME, "price": 25.50,
            "description": "An updated, even higher-quality widget."
        }
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.patch("/items/update_item", json=update_data, headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] == "Item updated successfully"
    assert response_body["body"]["price"] == 25.50


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        await test_add_item(client)
        response = await client.delete(f"/items/delete_item?itemName={TEST_ITEM_NAME}", headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] == "Item deleted successfully"