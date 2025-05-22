"""Test cases for Report endpoints."""


def test_create_report(_client):
    """Test creating a report."""
    response = _client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-04-21",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["type"] == "Monthly Report"
    assert data["content"] == "This is the content of the report."


def test_get_report(_client):
    """Test retrieving a report."""
    response = _client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-04-15",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = _client.get(f"/report/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Monthly Report"
    assert data["dateReport"] == "2025-04-15"
    assert data["content"] == "This is the content of the report."


def test_get_all_reports(_client):
    """Test retrieving all reports."""
    response = _client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-04-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = _client.get("/report/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_update_report(_client):
    """Test updating a report."""
    response = _client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-01-01",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = _client.put(
        f"/report/{report_id}",
        json={
            "type": "Updated Report",
            "dateReport": "2025-02-02",
            "content": "Updated content.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Updated Report"
    assert data["dateReport"] == "2025-02-02"
    assert data["content"] == "Updated content."


def test_delete_report(_client):
    """Test deleting a report."""
    response = _client.post(
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-03-03",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    report_id = data["id"]
    response = _client.delete(f"/report/{report_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Report deleted successfully"

    # Verify that the report no longer exists
    response = _client.get(f"/report/{report_id}")
    assert response.status_code == 404


def test_get_total_client_bills_route(_client):
    """Test retrieving all reports."""
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
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-04-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = _client.get("/bills/clients/month-total")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_get_top_client_spender_this_month(_client):
    """Test retrieving all reports."""
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
        "/report/",
        json={
            "type": "Monthly Report",
            "dateReport": "2025-04-12",
            "content": "This is the content of the report.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    response = _client.get("/bills/monthlySalesTotal")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
