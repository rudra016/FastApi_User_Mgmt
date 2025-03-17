import pytest
import httpx
import uuid

BASE_URL_AUTH = "http://localhost:8000"

@pytest.fixture(scope="session")
def test_client():
    """Create an HTTPX test client."""
    with httpx.Client() as client:
        yield client

@pytest.fixture(scope="session") 
def create_test_user(test_client):
    """Creates a test user once and reuses it for all tests."""
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser619@example.com",  
        "password": "testpassword123"
    }

  
    login_response = test_client.post(
        f"{BASE_URL_AUTH}/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )

    if login_response.status_code == 200:
        # If login is successful, return the existing user's token
        return {
            "token": login_response.json()["token"],
            "email": user_data["email"],
            "user_id": None  # User ID not needed if already exists
        }

 
    signup_response = test_client.post(f"{BASE_URL_AUTH}/auth/signup", json=user_data)
    assert signup_response.status_code == 201, f"Signup failed: {signup_response.json()}"
    
    user_id = signup_response.json()["id"]  # Capture user ID


    login_response = test_client.post(
        f"{BASE_URL_AUTH}/auth/login",
        json={"email": user_data["email"], "password": user_data["password"]}
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"
    
    return {
        "token": login_response.json()["token"],
        "email": user_data["email"],
        "user_id": user_id
    }
