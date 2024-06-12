import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "full_name": "Test User", "hashed_password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_read_user():
    response = client.post(
        "/users/",
        json={"email": "another@example.com", "full_name": "Another User", "hashed_password": "password456"}
    )
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "another@example.com"


def test_update_user():
    response = client.post(
        "/users/",
        json={"email": "updatable@example.com", "full_name": "Updatable User", "hashed_password": "password789"}
    )
    user_id = response.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"email": "updated@example.com", "full_name": "Updated User", "hashed_password": "newpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"


def test_delete_user():
    response = client.post(
        "/users/",
        json={"email": "deletable@example.com", "full_name": "Deletable User", "hashed_password": "password012"}
    )
    user_id = response.json()["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
