import httpx
import pytest

BASE_URL_ORDERS = "http://localhost:8001"

@pytest.fixture
def create_order(test_client, create_test_user):
    """Creates a test order and returns the order ID."""
    order_data = {
        "user_id": 40,
        "product_name": "Laptop",
        "quantity": 10,
        "price": 1200.50,
        "description": "Gaming Laptop Asus",
        "status": "pending"
    }
    response = test_client.post(f"{BASE_URL_ORDERS}/orders/create/", json=order_data)
    assert response.status_code == 201
    return response.json()

def test_create_order(test_client, create_order):
    """Test order creation."""
    assert "order" in create_order 
    assert "id" in create_order["order"] 

def test_get_orders(test_client, create_test_user):
    """Test retrieving orders."""
    headers = {"Authorization": f"Bearer {create_test_user['token']}"}
    response = test_client.get(f"{BASE_URL_ORDERS}/orders/list/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
