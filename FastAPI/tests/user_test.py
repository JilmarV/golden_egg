"""Test cases for User endpoints."""

# pylint: disable=import-error, no-name-in-module, too-few-public-methods, redefined-outer-name

# Standard library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Third-party
import pytest

# Application
from fastapi.testclient import TestClient
from app.main import app
from app.db.database import Base
from app.db.session import get_db


# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    """Creates a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Overrides the dependency to use the test database."""

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_create_user(client):
    """Test creating a user."""
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    assert response.status_code == 201
    response = client.post("/user/", 
                           json={
                               "name": "User", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail@Mail.com", 
                               "username":"user",
                               "password": "123",
                               "address": "Somewhere",
                               "enabled": True,
                                "role_ids": [1]
                               })
    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "User"


def test_get_user(client):
    """Test getting a user."""
    # First, create a user
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={
                               "name": "User", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail@Mail.com", 
                               "username":"user",
                               "password": "123",
                               "address": "Somewhere",
                               "enabled": True,
                                "role_ids": [1]
                               })
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Now, get the user
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_users(client):
    """Test getting all users."""
    # Create some users
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    client.post("/user/", json={
                               "name": "User1", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail2@Mail.com", 
                               "username":"user1",
                               "password": "1234",
                               "address": "Somewhere1",
                               "enabled": True,
                                "role_ids": [1]
                               })
    client.post("/user/", json={
                               "name": "User2", 
                               "phone_number": "3115070040", 
                               "email": "SomeEmail34@Mail.com", 
                               "username":"user2",
                               "password": "123455",
                               "address": "Somewhere123",
                               "enabled": True,
                                "role_ids": [1]
                               })

    # Get all users
    response = client.get("/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_user(client):
    """Test updating a user."""
    # First, create a user
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={
                               "name": "User", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail@Mail.com", 
                               "username":"user",
                               "password": "123",
                               "address": "Somewhere",
                               "enabled": True,
                                "role_ids": [1]
                               })
    assert response.status_code == 201
    user_id = response.json()["id"]
    # Now, update the user
    response = client.put(f"/user/{user_id}", json={
                               "name": "User2", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail34@Mail.com", 
                               "username":"user2",
                               "password": "123455",
                               "address": "Somewhere123",
                               "enabled": True,
                                "role_ids": [1]
                               })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User2"


def test_delete_user(client):
    """Test deleting a user."""
    # First, create a user
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/user/", json={
                               "name": "User", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail@Mail.com", 
                               "username":"user",
                               "password": "123",
                               "address": "Somewhere",
                               "enabled": True,
                                "role_ids": [1]
                               })
    assert response.status_code == 201
    user_id = response.json()["id"]
    # Now, delete the user
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"

def test_get_users_by_role(client):
    """Test getting all users."""
    # Create some users
    response = client.post("/role/", json={"name": "EMPLOYEE"})
    response = client.post("/role/", json={"name": "CUSTOMER"})
    client.post("/user/", json={
                               "name": "User1", 
                               "phone_number": "3115070080", 
                               "email": "SomeEmail2@Mail.com", 
                               "username":"user1",
                               "password": "1234",
                               "address": "Somewhere1",
                               "enabled": True,
                                "role_ids": [1]
                               })
    client.post("/user/", json={
                               "name": "User2", 
                               "phone_number": "3115070040", 
                               "email": "SomeEmail34@Mail.com", 
                               "username":"user2",
                               "password": "123455",
                               "address": "Somewhere123",
                               "enabled": True,
                                "role_ids": [1]
                               })
    client.post("/user/", json={
                               "name": "User2", 
                               "phone_number": "3115070040", 
                               "email": "SomeEmail34@Mail.com", 
                               "username":"user2",
                               "password": "123455",
                               "address": "Somewhere123",
                               "enabled": True,
                                "role_ids": [2]
                               })
    # Get all users
    response = client.get("/user/byrole/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1