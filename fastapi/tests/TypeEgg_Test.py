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


def test_create_typeEgg(client):
    response = client.post(
        "/typeEgg/", json={"name": "SupremeEgg"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg1"
    assert "id" in data 



def test_read_typeEggs(client):
    client.post(
        "/typeEgg/", json={"name": "SupremeEgg"}
    )
    response = client.get("/typeEgg/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


def test_read_typeEgg(client):
    create_response = client.post(
        "/typeEgg/", json={"name": "SupremeEgg"}
    )
    created_typeEgg = create_response.json()
    response = client.get(f"/items/{created_typeEgg['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SupremeEgg"


def test_update_typeEgg(client):
    create_response = client.post(
        "/typeEgg/", json={"name": "SupremeEgg"}
    )
    created_typeEgg= create_response.json()
    response = client.put(
        f"/typeEgg/{created_typeEgg['id']}",
        json={"name": "THESUPREMEEGG"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "THESUPREMEEGG"


def test_delete_typeEgg(client):
    create_response = client.post(
        "/typeEgg/", json={"name": "SupremeEgg"}
    )
    created_typeEgg = create_response.json()

    response = client.delete(f"/typeEgg/{created_typeEgg['id']}")
    assert response.status_code == 200

    get_response = client.get(f"/typeEgg/{created_typeEgg['id']}")
    assert get_response.status_code == 404