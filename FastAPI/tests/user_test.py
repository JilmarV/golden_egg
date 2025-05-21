"""Test cases for User endpoints."""

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
from app.User.user_model import User
from app.Role.role_model import Role
from app.Auth.auth_service import get_current_user, require_admin

def override_require_admin():
    user = User(id= 1,name ="admin", phone_number="3334445566", email= "Juas@Juas.com", username="admin", password="321",address="1",enable= True, roles=[Role(id=1, name="ADMIN")])
    return user

app.dependency_overrides[get_current_user] = override_require_admin
app.dependency_overrides[require_admin] = override_require_admin

@pytest.fixture
def client():
    yield TestClient(app)

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def _test_db():
    """Creates a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def _client(_test_db):
    """Overrides the dependency to use the test database."""

    def override_get_db():
        yield _test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

def test_override_direct():
    from app.Auth import auth_service
    from app.main import app
    assert auth_service.require_admin in app.dependency_overrides, "Override for require_admin is not active"


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
            "role_ids": [1],
        },
    )
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Now, get the user
    response = _client.get(f"/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User"


def test_get_all_users(_client):
    """Test getting all users."""
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
            "role_ids": [1],
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
            "role_ids": [1],
        },
    )

    # Get all users
    response = _client.get("/user/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2


def test_update_user(_client):
    """Test updating a user."""
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
            "role_ids": [1],
        },
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    # Now, update the user
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
            "role_ids": [1],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "User2"


def test_delete_user(_client):
    """Test deleting a user."""
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
            "role_ids": [1],
        },
    )
    assert response.status_code == 201
    user_id = response.json()["id"]
    # Now, delete the user
    response = _client.delete(f"/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User deleted successfully"


def test_get_users_by_role(_client):
    """Test getting all users."""
    # Create some users
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
            "role_ids": [1],
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
            "role_ids": [1],
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
    response = _client.get("/user/byrole/1")
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
