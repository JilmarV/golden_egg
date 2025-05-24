"""Test cases for Bill endpoints."""

def test_create_bill(_client):
    """Test creating a bill."""
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
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
    assert response.status_code == 201
    print(response.json())
    response = _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    assert response.status_code == 201
    response = _client.post(
        "/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1}
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["totalprice"] == 5000
    assert data["paid"] is False
    assert "id" in data


def test_read_bills(_client):
    """Test retrieving all bills."""
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
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
    assert response.status_code == 201
    response = _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post("/bill/", json={"totalprice": 2010, "paid": False, "order_id": 1})
    response = _client.get("/bill/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_bill(_client):
    """Test retrieving a specific bill."""
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
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
    create_response = _client.post(
        "/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1}
    )
    created_bill = create_response.json()
    response = _client.get(f"/bill/{created_bill['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 3000


def test_update_bill(_client):
    """Test updating a bill."""
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
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
    create_response = _client.post(
        "/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1}
    )
    created_bill = create_response.json()
    response = _client.put(
        f"/bill/{created_bill['id']}",
        json={"totalprice": 1500, "paid": True, "order_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 1500
    assert data["paid"] is True


def test_delete_bill(_client):
    """Test deleting a bill."""
    _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
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
    create_response = _client.post(
        "/bill/", json={"totalprice": 8000, "paid": False, "order_id": 1}
    )
    created_bill = create_response.json()
    response = _client.delete(f"/bill/{created_bill['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/bill/{created_bill['id']}")
    assert get_response.status_code == 404


def test_count_this_month_bills(_client):
    """Test counting bills for the current month."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3143333333",
            "email": "SomeEmail2@Mail.com",
            "username": "user2",
            "password": "123",
            "address": "Somewh2ere",
            "enabled": True,
            "role_ids": [1],
        },
    )
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
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 2,
        },
    )
    _client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = _client.post(
        "/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2}
    )
    print(response.json())
    response = _client.get("/bill/customer/countThisMonth")
    print(response.json())
    assert response.status_code == 200
    count = response.json()
    print(count)
    assert len(count) == 5


def test_best_client(_client):
    """Test the customer with the most bills."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3143333333",
            "email": "SomeEmail2@Mail.com",
            "username": "user2",
            "password": "123",
            "address": "Somewh2ere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    _client.post(
        "/user/",
        json={
            "name": "User2",
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
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 2,
        },
    )
    _client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    _client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = _client.get("/bill/customer/bestCustomer")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data == "User"


def test_get_all_company(_client):
    """Test the employees procesed bills."""
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/role/", json={"name": "ADMIN"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3143333333",
            "email": "SomeEmail2@Mail.com",
            "username": "user2",
            "password": "123",
            "address": "Somewh2ere",
            "enabled": True,
            "role_ids": [1],
        },
    )
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
            "role_ids": [2],
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 2,
        },
    )
    _client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    _client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = _client.get("/bill/company/getAllOfCompany")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 5
    print(response.json())


def test_get_all_from_customers(_client):
    """Test the customer's bills."""
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3143333333",
            "email": "SomeEmail2@Mail.com",
            "username": "user2",
            "password": "123",
            "address": "Somewh2ere",
            "enabled": True,
            "role_ids": [1],
        },
    )
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
            "role_ids": [2],
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 2,
        },
    )
    _client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 2})
    _client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    _client.post("/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2})
    response = _client.get("/bill/customer/getAllOfCustomers")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 3
    print(response.json())


def test_get_all_monthly_from_customer(_client):
    """Test the customer with the most bills."""
    _client.post("/role/", json={"name": "EMPLOYEE"})
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
        "/user/",
        json={
            "name": "User",
            "phone_number": "3143333333",
            "email": "SomeEmail2@Mail.com",
            "username": "user2",
            "password": "123",
            "address": "Somewhere2",
            "enabled": True,
            "role_ids": [2],
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 1,
        },
    )
    _client.post(
        "/order/",
        json={
            "totalPrice": 20100,
            "state": "pending",
            "user_id": 2,
        },
    )
    _client.post("/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1})
    _client.post("/bill/", json={"totalprice": 4000, "paid": False, "order_id": 2})
    response = _client.post(
        "/bill/", json={"totalprice": 5000, "paid": False, "order_id": 2}
    )
    response = _client.get("/bill/company/monthlySalesTotal")
    print(response.json())
    assert response.status_code == 200
    print(response.json())
