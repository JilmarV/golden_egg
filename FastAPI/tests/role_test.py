"""Test cases for Role endpoints."""


def test_create_role(_client):
    """Test creating a role."""
    response = _client.post("/role/", json={"name": "Admin"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Admin"


def test_get_role(_client):
    """Test getting a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]

    # Now, get the role
    response = _client.get(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_roles(_client):
    """Test getting all roles."""
    # Create some roles
    _client.post("/role/", json={"name": "Admin"})
    _client.post("/role/", json={"name": "User"})

    # Get all roles
    response = _client.get("/role/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_role(_client):
    """Test updating a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, update the role
    response = _client.put(f"/role/{role_id}", json={"name": "SuperUser"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SuperUser"


def test_delete_role(_client):
    """Test deleting a role."""
    # First, create a role
    response = _client.post("/role/", json={"name": "User"})
    assert response.status_code == 201
    role_id = response.json()["id"]
    # Now, delete the role
    response = _client.delete(f"/role/{role_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Role deleted successfully"
