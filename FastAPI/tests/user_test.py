"""Test cases for User endpoints."""


def test_create_user(_client):
    """Test creating a user."""
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    assert response.status_code == 201
    response = _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3115070080",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [1],
        },
    )
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "User"


def test_get_user(_client):
    """Test getting a user."""

    response = _client.post("/role/", json={"name": "ADMIN"})
    assert response.status_code == 201

    response = _client.post(
        "/user/",
        json={
            "name": "Admin User",
            "phone_number": "3000000000",
            "email": "admin@mail.com",
            "username": "adminuser",
            "password": "admin123",
            "address": "HQ",
            "enabled": True,
            "role_ids": [1],  
        },
    )
    assert response.status_code == 201

    response = _client.post(
        "/login",
        data={"username": "adminuser", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}
    # First, create a user
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3115070080",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [2],
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Now, get the user
    response = _client.get(f"/user/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_users(_client):
    """Test getting all users."""

    
    response = _client.post("/role/", json={"name": "ADMIN"})
    assert response.status_code == 201

    response = _client.post(
        "/user/",
        json={
            "name": "Admin User",
            "phone_number": "3000000000",
            "email": "admin@mail.com",
            "username": "adminuser",
            "password": "admin123",
            "address": "HQ",
            "enabled": True,
            "role_ids": [1],  
        },
    )
    assert response.status_code == 201

    response = _client.post(
        "/login",
        data={"username": "adminuser", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    # Create some users
    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    _client.post(
        "/user/",
        json={
            "name": "User1",
            "phone_number": "3115070080",
            "email": "SomeEmail2@Mail.com",
            "username": "user1",
            "password": "1234",
            "address": "Somewhere1",
            "enabled": True,
            "role_ids": [2],
        },
    )
    _client.post(
        "/user/",
        json={
            "name": "User2",
            "phone_number": "3115070040",
            "email": "SomeEmail34@Mail.com",
            "username": "user2",
            "password": "123455",
            "address": "Somewhere123",
            "enabled": True,
            "role_ids": [2],
        },
    )

    # Get all users
    response = _client.get("/user/", headers= auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_user(_client):
    """Test updating a user."""
    
    response = _client.post("/role/", json={"name": "ADMIN"})
    assert response.status_code == 201

    response = _client.post(
        "/user/",
        json={
            "name": "Admin User",
            "phone_number": "3000000000",
            "email": "admin@mail.com",
            "username": "adminuser",
            "password": "admin123",
            "address": "HQ",
            "enabled": True,
            "role_ids": [1],  
        },
    )
    assert response.status_code == 201

    response = _client.post(
        "/login",
        data={"username": "adminuser", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3115070080",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [2],
        },
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    response = _client.put(
        f"/user/{user_id}",
        json={
            "name": "User2",
            "phone_number": "3115070080",
            "email": "SomeEmail34@Mail.com",
            "username": "user2",
            "password": "123455",
            "address": "Somewhere123",
            "enabled": True,
            "role_ids": [2],
        }, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User2"


def test_delete_user(_client):
    """Test deleting a user."""
    response = _client.post("/role/", json={"name": "ADMIN"})
    assert response.status_code == 201

    response = _client.post(
        "/user/",
        json={
            "name": "Admin User",
            "phone_number": "3000000000",
            "email": "admin@mail.com",
            "username": "adminuser",
            "password": "admin123",
            "address": "HQ",
            "enabled": True,
            "role_ids": [1],  
        },
    )
    assert response.status_code == 201

    response = _client.post(
        "/login",
        data={"username": "adminuser", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post(
        "/user/",
        json={
            "name": "User",
            "phone_number": "3115070080",
            "email": "SomeEmail@Mail.com",
            "username": "user",
            "password": "123",
            "address": "Somewhere",
            "enabled": True,
            "role_ids": [2],
        },
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    response = _client.delete(f"/user/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"


def test_get_users_by_role(_client):
    """Test getting all users."""
    response = _client.post("/role/", json={"name": "ADMIN"})
    assert response.status_code == 201

    response = _client.post(
        "/user/",
        json={
            "name": "Admin User",
            "phone_number": "3000000000",
            "email": "admin@mail.com",
            "username": "adminuser",
            "password": "admin123",
            "address": "HQ",
            "enabled": True,
            "role_ids": [1],  
        },
    )
    assert response.status_code == 201

    response = _client.post(
        "/login",
        data={"username": "adminuser", "password": "admin123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    token = response.json()["access_token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    response = _client.post("/role/", json={"name": "EMPLOYEE"})
    response = _client.post("/role/", json={"name": "CUSTOMER"})
    _client.post(
        "/user/",
        json={
            "name": "User1",
            "phone_number": "3115070080",
            "email": "SomeEmail2@Mail.com",
            "username": "user1",
            "password": "1234",
            "address": "Somewhere1",
            "enabled": True,
            "role_ids": [2],
        },
    )
    _client.post(
        "/user/",
        json={
            "name": "User2",
            "phone_number": "3115070040",
            "email": "SomeEmail34@Mail.com",
            "username": "user2",
            "password": "123455",
            "address": "Somewhere123",
            "enabled": True,
            "role_ids": [3],
        },
    )
    _client.post(
        "/user/",
        json={
            "name": "User2",
            "phone_number": "3115070040",
            "email": "SomeEmail34@Mail.com",
            "username": "user2",
            "password": "123455",
            "address": "Somewhere123",
            "enabled": True,
            "role_ids": [3],
        },
    )
    # Get all users
    response = _client.get("/user/byrole/3", headers = auth_headers)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
