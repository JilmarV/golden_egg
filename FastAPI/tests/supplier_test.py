"""Test cases for the supplier API."""


def test_create_supplier(_client):
    """Test creating a supplier."""
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Supplier2"


def test_get_supplier(_client):
    """Test getting a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier", "address": "Someplace"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]

    # Now, get the supplier
    response = _client.get(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier"


def test_get_all_suppliers(_client):
    """Test getting all suppliers."""
    # Create some suppliers
    _client.post("/supplier/", json={"name": "Supplier1", "address": "Someplace"})
    _client.post("/supplier/", json={"name": "Supplier2", "address": "Somewhere"})

    # Get all suppliers
    response = _client.get("/supplier/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_supplier(_client):
    """Test updating a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier1", "address": "Someplace"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, update the supplier
    response = _client.put(
        f"/supplier/{supplier_id}", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Supplier2"


def test_delete_supplier(_client):
    """Test deleting a supplier."""
    # First, create a supplier
    response = _client.post(
        "/supplier/", json={"name": "Supplier2", "address": "Somewhere"}
    )
    assert response.status_code == 201
    supplier_id = response.json()["id"]
    # Now, delete the supplier
    response = _client.delete(f"/supplier/{supplier_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Supplier deleted successfully"
