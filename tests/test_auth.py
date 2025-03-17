import httpx
import uuid
BASE_URL_AUTH = "http://localhost:8000"


def test_signup(test_client):
    """Test user registration."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"testuser-{uuid.uuid4()}@example.com",  # Unique email per run
        "password": "securepassword"
    }
    response = test_client.post(f"{BASE_URL_AUTH}/auth/signup", json=user_data)
    assert response.status_code == 201, f"Signup failed: {response.json()}"

def test_login(test_client, create_test_user):
    """Test user login."""
    user_data = {
        "email": create_test_user["email"],
        "password": "testpassword123"
    }
    response = test_client.post(f"{BASE_URL_AUTH}/auth/login", json=user_data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_get_user_details(test_client, create_test_user):
    """Test retrieving user details with authentication."""
    headers = {"Authorization": f"Bearer {create_test_user['token']}"}
    response = test_client.get(f"{BASE_URL_AUTH}/protected", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"]["email"] == create_test_user["email"]
