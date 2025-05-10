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


def test_create_bill(client):
    response = client.post(
        "/bill/", json={"totalprice": 5000, "paid": False, "order_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 5000
    assert data["paid"] == False
    assert "id" in data 



def test_read_bills(client):
    client.post(
        "/bill/", json={"totalprice": 2000, "paid": False, "order_id": 1}
    )
    response = client.get("/bill/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_bill(client):
    create_response = client.post(
        "/bill/", json={"totalprice": 3000, "paid": False, "order_id": 1}
    )
    created_bill = create_response.json()
    response = client.get(f"/bill/{created_bill['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 3000


def test_update_bill(client):
    create_response = client.post(
        "/bill/", json={"totalprice": 1000, "paid": False, "order_id": 1}
    )
    created_bill= create_response.json()
    response = client.put(
        f"/bill/{created_bill['id']}",
        json={"totalprice": 1500, "paid": True, "order_id": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["totalprice"] == 1500
    assert data["paid"] == True


def test_delete_bill(client):
    create_response = client.post(
        "/bill/", json={"totalprice": 8000, "paid": False, "order_id": 1}
    )
    created_bill = create_response.json()

    response = client.delete(f"/bill/{created_bill['id']}")
    assert response.status_code == 200

    get_response = client.get(f"/bill/{created_bill['id']}")
    assert get_response.status_code == 404