import pytest
import pytest_asyncio
import uuid  
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from main import app
from app.db.models.user import USER_SESSION, UserRole
from app.db.session import DataBasePool

# --- Test Constants ---
TEST_OWNER_ID = "3e592b3b-5064-4ff5-9fcf-2bf8382972fe"
TEST_SHOP_ID = "07446c46-7775-4c99-a29e-79843fb69f93"

# --- Mock Data ---
mock_user_session = USER_SESSION(
    pk="test_session_token",
    email="testvendor@example.com",
    role=UserRole.VENDOR,
    ip="127.0.0.1", browser="test-client", os="pytest",
    created_at=1672531200, expired_at=9999999999
)

@pytest_asyncio.fixture
async def client():
    await DataBasePool.setup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    await DataBasePool.teardown()

@pytest.mark.asyncio
async def test_create_shop(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        unique_shop_name = f"My Test Shop {uuid.uuid4()}"
        
        shop_data = {
            "owner_id": TEST_OWNER_ID, "fullName": "Test Vendor",
            "shopName": unique_shop_name,  
            "address": "101 Idempotent Road",
            "contact": "5566778899", "latitude": 23.83, "longitude": 91.27,
            "email": "testvendor-final-ci@example.com", "password": "a_secure_password"
        }
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.post("/shops/create_shop", json=shop_data, headers=headers)

    # The assertion now correctly expects 201, as the shop will always be new.
    assert response.status_code == 201
    assert response.json()["message"] == "Shop created successfully"

@pytest.mark.asyncio
async def test_get_shop_by_id(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get(f"/shops/{TEST_SHOP_ID}", headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert response_body["message"] in ["Shop retrieved", "Shop retrieved from cache"]
    assert response_body["body"]["shopName"] == "Raju General Store"


@pytest.mark.asyncio
async def test_view_shop_by_owner(client: AsyncClient):
    with patch("app.db.session.DB.getUserSession", new_callable=AsyncMock, return_value=mock_user_session):
        headers = {"Cookie": "shopNear_=test_session_token"}
        response = await client.get(f"/shops/view_shop?owner_id={TEST_OWNER_ID}", headers=headers)

    assert response.status_code == 200
    response_body = response.json()
    assert isinstance(response_body["body"], list)
    assert len(response_body["body"]) > 0
    assert response_body["body"][0]["shopName"] == "Raju General Store"