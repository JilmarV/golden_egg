import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi import app
from app.db.database import Base
from app.db.session import get_db

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///:memory:"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_inventory(client):
    response = client.post(
        "/inventory/", json={"nameProduct": "Product", "availableQuantity": 10, "price": 100, "expirationDate": "2025-01-01"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Product"
    assert data["availableQuantity"] == 10
    assert data["price"] == 100
    assert data["expirationDate"] == "2025-01-01"
    assert "id" in data 



def test_read_inventorys(client):
    client.post(
        "/inventory/", json={"nameProduct": "Product", "availableQuantity": 10, "price": 100, "expirationDate": "2025-02-01"}
    )
    response = client.get("/inventory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_inventory(client):
    create_response = client.post(
        "/inventory/", json={"nameProduct": "Product", "availableQuantity": 10, "price": 100, "expirationDate": "2025-03-01"}
    )
    created_inventory = create_response.json()
    response = client.get(f"/items/{created_inventory['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Product"
    assert data["availableQuantity"] == 10
    assert data["price"] == 100
    assert data["expirationDate"] == "2025-03-01"


def test_update_inventory(client):
    create_response = client.post(
        "/inventory/", json={"nameProduct": "Product", "availableQuantity": 10, "price": 100, "expirationDate": "2025-04-01"}
    )
    created_inventory= create_response.json()
    response = client.put(
        f"/inventory/{created_inventory['id']}",
        json={"nameProduct": "Product2", "availableQuantity": 12, "price": 200, "expirationDate": "2025-05-01"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nameProduct"] == "Product2"
    assert data["availableQuantity"] == 12
    assert data["price"] == 100
    assert data["expirationDate"] == "2025-03-01"


def test_delete_inventory(client):
    create_response = client.post(
        "/inventory/", json={"nameProduct": "Product2", "availableQuantity": 12, "price": 200, "expirationDate": "2025-05-01"}
    )
    created_inventory = create_response.json()

    response = client.delete(f"/inventory/{created_inventory['id']}")
    assert response.status_code == 200

    get_response = client.get(f"/inventory/{created_inventory['id']}")
    assert get_response.status_code == 404