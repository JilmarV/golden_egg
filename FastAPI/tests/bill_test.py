from datetime import datetime

def make_bill_payload(totalprice, paid, order_id):
    return {
        "totalprice": totalprice,
        "paid": paid,
        "order_id": order_id,
        "issueDate": datetime.now().isoformat(),
    }

def test_create_bill(_client):
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/user/", json={
        "name": "User",
        "phone_number": "3133333333",
        "email": "mail@mail.com",
        "username": "user_create",
        "password": "123",
        "address": "Somewhere",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={
        "totalPrice": 20100,
        "state": "pending",
        "user_id": 1,
    })
    response = _client.post("/bill/", json=make_bill_payload(5000, False, 1))
    assert response.status_code == 201
    data = response.json()
    assert data["totalprice"] == 5000
    assert data["paid"] is False
    assert data.get("id") is not None

def test_read_bill(_client):
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/user/", json={
        "name": "User",
        "phone_number": "3111111111",
        "email": "mail2@mail.com",
        "username": "user_read",
        "password": "123",
        "address": "City",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={"totalPrice": 10000, "state": "pending", "user_id": 1})
    response = _client.post("/bill/", json=make_bill_payload(3000, False, 1))
    bill = response.json()
    assert "id" in bill
    get_response = _client.get(f"/bill/{bill['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["totalprice"] == 3000

def test_update_bill(_client):
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/user/", json={
        "name": "User",
        "phone_number": "3222222222",
        "email": "mail3@mail.com",
        "username": "user_update",
        "password": "123",
        "address": "Village",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={"totalPrice": 9000, "state": "pending", "user_id": 1})
    response = _client.post("/bill/", json=make_bill_payload(1000, False, 1))
    bill = response.json()
    response = _client.put(f"/bill/{bill['id']}", json=make_bill_payload(1500, True, 1))
    assert response.status_code == 200
    updated = response.json()
    assert updated["totalprice"] == 1500
    assert updated["paid"] is True

def test_delete_bill(_client):
    _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post("/user/", json={
        "name": "User",
        "phone_number": "3333333333",
        "email": "mail4@mail.com",
        "username": "user_delete",
        "password": "123",
        "address": "Home",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={"totalPrice": 9500, "state": "pending", "user_id": 1})
    response = _client.post("/bill/", json=make_bill_payload(8000, False, 1))
    bill = response.json()
    delete_response = _client.delete(f"/bill/{bill['id']}")
    assert delete_response.status_code == 200
    get_response = _client.get(f"/bill/{bill['id']}")
    assert get_response.status_code == 404

def test_count_this_month_bills(_client):
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={
        "name": "Client1",
        "phone_number": "3011111111",
        "email": "client1@mail.com",
        "username": "client1",
        "password": "123",
        "address": "Addr1",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/user/", json={
        "name": "Client2",
        "phone_number": "3022222222",
        "email": "client2@mail.com",
        "username": "client2",
        "password": "123",
        "address": "Addr2",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={"totalPrice": 20000, "state": "pending", "user_id": 1})
    _client.post("/order/", json={"totalPrice": 20000, "state": "pending", "user_id": 2})
    _client.post("/bill/", json=make_bill_payload(1000, False, 1))
    _client.post("/bill/", json=make_bill_payload(2000, False, 1))
    _client.post("/bill/", json=make_bill_payload(3000, False, 1))
    _client.post("/bill/", json=make_bill_payload(4000, False, 2))
    _client.post("/bill/", json=make_bill_payload(5000, False, 2))
    
    response = _client.get("/bill/customer/countThisMonth")
    assert response.status_code == 200
    count = response.json()
    assert count == 5

def test_best_client(_client):
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={
        "name": "TopClient",
        "phone_number": "3033333333",
        "email": "top@mail.com",
        "username": "topclient",
        "password": "123",
        "address": "TopCity",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/user/", json={
        "name": "RegularClient",
        "phone_number": "3044444444",
        "email": "reg@mail.com",
        "username": "regclient",
        "password": "123",
        "address": "RegCity",
        "enabled": True,
        "role_ids": [1],
    })
    _client.post("/order/", json={"totalPrice": 20000, "state": "pending", "user_id": 1})
    _client.post("/order/", json={"totalPrice": 20000, "state": "pending", "user_id": 2})
    _client.post("/bill/", json=make_bill_payload(1000, False, 1))
    _client.post("/bill/", json=make_bill_payload(2000, False, 1))
    _client.post("/bill/", json=make_bill_payload(3000, False, 1))
    _client.post("/bill/", json=make_bill_payload(4000, False, 2))
    _client.post("/bill/", json=make_bill_payload(5000, False, 2))
    
    response = _client.get("/bill/customer/bestCustomer")
    assert response.status_code == 200
    assert response.json() == "TopClient"
