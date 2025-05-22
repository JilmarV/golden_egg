"""Test cases for Order endpoints."""


def test_create_orderEgg(_client):
    """Test creating an orderEgg."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    _client.post("/order/",json={"totalPrice": 40000,"state": "pending","user_id": 1})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/egg/",json={"avalibleQuantity": 30,"expirationDate": "2026-02-01","entryDate": "2025-05-21","sellPrice": 100,"entryPrice": 90,"color": "White","type_egg_id": 1,"supplier_id": 1})
    response = _client.post(
        "/orderegg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["quantity"] == 30
    assert data["unit_price"] == 900
    assert data["sub_total"] == 180000
    assert "id" in data
    assert data["order_id"] == 1


def test_get_orderEggs(_client):
    """Test retrieving all orderEggs."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    _client.post("/order/",json={"totalPrice": 40000,"state": "pending","user_id": 1})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/egg/",json={"avalibleQuantity": 30,"expirationDate": "2026-02-01","entryDate": "2025-05-21","sellPrice": 100,"entryPrice": 90,"color": "White","type_egg_id": 1,"supplier_id": 1})
    _client.post(
        "/orderegg/",
        json={
            "quantity": 30,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    response = _client.get("/orderegg/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_orderEgg(_client):
    """Test retrieving a specific orderEgg."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    _client.post("/order/",json={"totalPrice": 40000,"state": "pending","user_id": 1})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/egg/",json={"avalibleQuantity": 30,"expirationDate": "2026-02-01","entryDate": "2025-05-21","sellPrice": 100,"entryPrice": 90,"color": "White","type_egg_id": 1,"supplier_id": 1})
    response = _client.post(
        "/orderegg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = _client.get(f"/orderegg/{created_orderEgg['id']}")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 33


def test_update_orderEgg(_client):
    """Test updating an orderEgg."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    _client.post("/order/",json={"totalPrice": 40000,"state": "pending","user_id": 1})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/egg/",json={"avalibleQuantity": 30,"expirationDate": "2026-02-01","entryDate": "2025-05-21","sellPrice": 100,"entryPrice": 90,"color": "White","type_egg_id": 1,"supplier_id": 1})
    response = _client.post(
        "/orderegg/",
        json={
            "quantity": 33,
            "unit_price": 900,
            "sub_total": 180000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = _client.put(
        f"/orderegg/{created_orderEgg['id']}",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 44
    assert data["unit_price"] == 180
    assert data["sub_total"] == 240000


def test_delete_orderEgg(_client):
    """Test deleting an orderEgg."""
    _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post("/user/", json={"name": "User", "phone_number": "3133333333", "email": "SomeEmail@Mail.com", "username":"user","password": "123","address": "Somewhere","enabled": True, "role_ids": [1]})
    _client.post("/order/",json={"totalPrice": 40000,"state": "pending","user_id": 1})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/egg/",json={"avalibleQuantity": 30,"expirationDate": "2026-02-01","entryDate": "2025-05-21","sellPrice": 100,"entryPrice": 90,"color": "White","type_egg_id": 1,"supplier_id": 1})
    response = _client.post(
        "/orderegg/",
        json={
            "quantity": 44,
            "unit_price": 180,
            "sub_total": 240000,
            "egg_id": 1,
            "order_id": 1
        },
    )
    created_orderEgg = response.json()
    response = _client.delete(f"/orderegg/{created_orderEgg['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/orderegg/{created_orderEgg['id']}")
    assert get_response.status_code == 404
