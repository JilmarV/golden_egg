"""Test cases for Egg endpoints."""


def test_create_egg(_client):
    """Test creating an egg."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    print(response.json())
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    print(response.json())
    response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["color"] == "White"
    assert data["expirationDate"] == "2026-02-01"
    assert "id" in data


def test_read_eggs(_client):
    """Test retrieving all eggs."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    response = _client.get("/egg/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_egg(_client):
    """Test retrieving a specific egg."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    create_response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    created_egg = create_response.json()
    response = _client.get(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "White"
    assert data["expirationDate"] == "2026-02-01"


def test_update_egg(_client):
    """Test updating an egg."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    create_response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    created_egg = create_response.json()
    response = _client.put(
        f"/egg/{created_egg['id']}",
        json={
            "avalibleQuantity": 90,
            "expirationDate": "2025-09-01",
            "entryDate": "2025-05-21",
            "sellPrice": 900,
            "entryPrice": 9000,
            "color": "Brown",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["color"] == "Brown"
    assert data["expirationDate"] == "2025-09-01"


def test_delete_egg(_client):
    """Test deleting an egg."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    print(response.json())
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    print(response.json())
    create_response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    created_egg = create_response.json()
    response = _client.delete(f"/egg/{created_egg['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/egg/{created_egg['id']}")
    assert get_response.status_code == 404


def test_get_egg_stock(_client):
    """Test retrieving all eggs."""
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _client.post("/typeeggs/", json={"name": "AA"})
    response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 2,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 91,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1
        }
    )
    assert response.status_code == 201
    response = _client.get("/egg/search/count_this_month")
    data = response.json()
    print(data)
    assert data >= 2

def test_get_month_egg(_client):
    """Test retrieving all eggs."""
    _client.post(
        "/supplier/",json={"name": "Supplier2", "address": "Somewhere"}
    )
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    _response = _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 30,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    assert _response.status_code == 201
    _client.post(
        "/egg/",
        json={
            "avalibleQuantity": 91,
            "expirationDate": "2026-02-01",
            "entryDate": "2025-05-21",
            "sellPrice": 100,
            "entryPrice": 90,
            "color": "White",
            "type_egg_id": 1,
            "supplier_id": 1,
        },
    )
    response = _client.get("/egg/search/count_this_month")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data == 2