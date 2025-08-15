import pytest
import pytest_asyncio
import uuid
from httpx import AsyncClient, ASGITransport

from main import app
from app.db.session import DataBasePool

# --- Pytest Fixture ---
@pytest_asyncio.fixture
async def client():
    """Manages the app lifecycle for tests, including DB setup and teardown."""
    await DataBasePool.setup()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    await DataBasePool.teardown()

# --- Auth API Tests ---

@pytest.mark.asyncio
async def test_user_signup_success(client: AsyncClient):
    """Test a new user can successfully sign up."""
    # Generate a unique email for each test run to ensure idempotency
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    user_data = {
        "fullName": "Test User",
        "email": unique_email,
        "password": "a_strong_password"
    }
    response = await client.post("/users/signup/user", json=user_data)
    
    assert response.status_code == 201
    response_body = response.json()
    assert response_body["message"] == "User registered successfully"
    assert response_body["body"]["email"] == unique_email


@pytest.mark.asyncio
async def test_user_signup_duplicate_email(client: AsyncClient):
    """Test that signing up with a duplicate email is forbidden."""
    unique_email = f"testuser_{uuid.uuid4()}@example.com"
    user_data = {"fullName": "Test User", "email": unique_email, "password": "a_strong_password"}

    # First, create the user successfully
    response1 = await client.post("/users/signup/user", json=user_data)
    assert response1.status_code == 201

    # Second, attempt to create the same user again
    response2 = await client.post("/users/signup/user", json=user_data)
    assert response2.status_code == 403 # 403 Forbidden is used for this in the app
    assert "Email already registered" in response2.json()["message"]


@pytest.mark.asyncio
async def test_login_and_logout(client: AsyncClient):
    """Test the full login, auth check, and logout flow."""
    # 1. Arrange: Create a new user to log in with
    unique_email = f"testlogin_{uuid.uuid4()}@example.com"
    password = "a_very_secure_password"
    user_data = {"fullName": "Login Test User", "email": unique_email, "password": password}
    
    signup_response = await client.post("/users/signup/user", json=user_data)
    assert signup_response.status_code == 201

    # 2. Act: Log in with the new user's credentials
    login_data = {"email": unique_email, "password": password}
    login_response = await client.post("/users/login", json=login_data)

    # 3. Assert: Check for a successful login
    assert login_response.status_code == 200
    assert "User logged in successfully" in login_response.json()["message"]
    # Verify that a session cookie was set
    assert "shopNear_" in login_response.cookies

    # 4. Act: Use the session cookie to check auth status
    auth_cookies = {"shopNear_": login_response.cookies["shopNear_"]}
    auth_response = await client.get("/users/auth", cookies=auth_cookies)

    # 5. Assert: Verify the auth status is valid
    assert auth_response.status_code == 200
    assert "Session is valid" in auth_response.json()["message"]
    assert auth_response.json()["body"]["email"] == unique_email
    
    # 6. Act: Use the same cookie to log out
    logout_response = await client.post("/users/logout", cookies=auth_cookies)
    
    # 7. Assert: Verify successful logout and cookie deletion
    assert logout_response.status_code == 200
    assert "Logged out successfully" in logout_response.json()["message"]
    # Check that the Set-Cookie header is trying to expire the cookie
    assert 'Max-Age=0' in logout_response.headers['set-cookie']


@pytest.mark.asyncio
async def test_login_failure_wrong_password(client: AsyncClient):
    """Test that login fails with an incorrect password."""
    login_data = {"email": "user-does-not-exist@example.com", "password": "wrong_password"}
    response = await client.post("/users/login", json=login_data)

    assert response.status_code == 401
    assert "Account not found" in response.json()["message"]