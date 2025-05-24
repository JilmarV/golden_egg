"""Test cases for Order endpoints."""

def test_create_order(_client):
    """Test creating an order."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    response = _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["totalPrice"] == 20100
    assert data["state"] == "pending"
    assert "id" in data
    assert data["user_id"] == 1


def test_get_orders(_client):
    """Test retrieving all orders."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    response = _client.get("/order/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_order(_client):
    """Test retrieving a specific order."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    response = _client.post(
        "/order/",
        json={"totalPrice": 40000, "state": "pending", "user_id": 1},
    )
    created_order = response.json()
    response = _client.get(f"/order/{created_order['id']}")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 40000


def test_update_order(_client):
    """Test updating an order."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    response = _client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    assert response.status_code == 201
    data = response.json()
    order_id = data["id"]
    response = _client.put(
        f"/order/{order_id}",
        json={
            "totalPrice": 50000,
            "state": "shipped",
            "user_id": 1,
        },
    )

    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 50000
    assert data["state"] == "shipped"
    assert data["user_id"] == 1


def test_delete_order(_client):
    """Test deleting an order."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    response = _client.post(
        "/order/",
        json={
            "totalPrice": 40000,
            "state": "pending",
            "user_id": 1,
        },
    )
    created_order = response.json()
    response = _client.delete(f"/order/{created_order['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/order/{created_order['id']}")
    assert get_response.status_code == 404
    

def test_get_orders_year_month(_client):
    """Test retrieving a specific order."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3133333333",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    response = _client.post(
        "/order/",
        json={"totalPrice": 40000, "state": "pending", "user_id": 1},
    )
    response = _client.post(
        "/order/",
        json={"totalPrice": 30000, "state": "pending", "user_id": 1},
    )
    response = _client.post(
        "/order/",
        json={"totalPrice": 20000, "state": "pending", "user_id": 1},
    )
    created_order = response.json()
    response = _client.get("/order/search/totalOrdersMonth", params={"year": 2025, "month": 5})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3