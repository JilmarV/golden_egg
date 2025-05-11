import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.app.main import app
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

def test_create_order(client):
    response = client.post(
        "/order/", json={"totalPrice": 20000, "orderDate": "2025-05-01", "state": "pending", "user_id": 1, }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 20000
    assert data["orderDate"] == "2025-05-01"
    assert data["state"] == "pending"
    assert "id" in data
    assert "user_id" in data
    assert data["user_id"] == 1
    
def test_get_orders(client):
    client.post(
        "/order/", json={"totalPrice": 40000, "orderDate": "2025-04-29", "state": "pending", "user_id": 1, }
    )
    response = client.get("/order/")
    assert response.status_code == 200
    data = response.json()
    
def test_get_order(client):
    response = client.post(
        "/order/", json={"totalPrice": 40000, "orderDate": "2025-04-29", "state": "pending", "user_id": 1, }
    )
    created_order = response.json()

    response = client.get(f"/order/{created_order['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 40000
    
def test_update_order(client):
    client.post(
        "/order/", json={"totalPrice": 40000, "orderDate": "2025-04-29", "state": "pending", "user_id": 1, }
    )
    response = client.post(
        "/order/", json={"totalPrice": 40000, "orderDate": "2025-04-29", "state": "pending", "user_id": 1, }
    )
    created_order = response.json()
    response = client.put(
        f"/order/{created_order['id']}", json={"totalPrice": 50000, "orderDate": "2025-04-30", "state": "shipped", "user_id": 1, }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalPrice"] == 50000
    assert data["orderDate"] == "2025-04-30"
    assert data["state"] == "shipped"
    assert data["user_id"] == 1
    
def test_delete_order(client):
    create_response = client.post(
        "/order/", json={"totalPrice": 40000, "orderDate": "2025-04-29", "state": "pending", "user_id": 1, }
    )
    reated_order = create_response.json()

    response = client.delete(f"/order/{reated_order['id']}")
    assert response.status_code == 200

    get_response = client.get(f"/order/{reated_order['id']}")
    assert get_response.status_code == 404
