"""Test cases for TypeEgg endpoints."""


def test_create_type_egg(_client):
    """Test creating a type egg."""
    response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "SupremeEgg"
    assert "id" in data


def test_read_type_eggs(_client):
    """Test retrieving all type eggs."""
    _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    response = _client.get("/typeeggs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_type_egg(_client):
    """Test retrieving a specific type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.get(f"/typeeggs/{created_type_egg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg"


def test_update_type_egg(_client):
    """Test updating a type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.put(
        f"/typeeggs/{created_type_egg['id']}", json={"name": "GoldenEgg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "GoldenEgg"


def test_delete_type_egg(_client):
    """Test deleting a type egg."""
    create_response = _client.post("/typeeggs/", json={"name": "SupremeEgg"})
    created_type_egg = create_response.json()
    response = _client.delete(f"/typeeggs/{created_type_egg['id']}")
    assert response.status_code == 200
    get_response = _client.get(f"/typeeggs/{created_type_egg['id']}")
    assert get_response.status_code == 404
