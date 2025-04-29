from fastapi.testclient import TestClient
from pytest import fixture as py_fixture

from api.models import UserCreate, User
from api.tests.conftest import *

@py_fixture
def mock_user(session):
    user = UserCreate(
        username="mock",
    )
    db_user = User.model_validate(user)
    session.add(db_user)
    db_user.is_admin = False
    db_user.auth_token = "mock_token"
    session.commit()
    session.refresh(db_user)
    return db_user


def test_validate_token_invalid_user(client: TestClient):
    # Mock token validation
    response = client.get("/validate_token", headers={"Authorization": "Bearer mock_token"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token or user not found."


def test_validate_token_valid_user(client: TestClient, mock_user):
    # Mock token validation
    response = client.get("/validate_token",
                          headers={"Authorization": f"Bearer {mock_user.auth_token}"}
                          )
    assert response.status_code == 200
    assert response.json() == f"{mock_user.username}, Your token is valid."


def test_get_users(client: TestClient):
    # Test user retrieval
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client: TestClient):
    # Test user creation
    user_data = {"username": "test_user"}
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "test_user"


def test_create_user_duplicate(client: TestClient):
    # Test duplicate user creation
    user_data = {"username": "test_user"}
    client.post("/user", json=user_data)  # Create user first
    response = client.post("/user", json=user_data)  # Attempt duplicate creation
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists."


def test_get_token(client: TestClient):
    # Test token retrieval
    user_data = {"username": "test_user"}
    client.post("/user", json=user_data)  # Create user first
    response = client.get(f"/get_token/{user_data['username']}")
    assert response.status_code == 200
    assert "auth_token" in response.json()


def test_get_token_user_not_found(client: TestClient):
    # Test token retrieval for non-existent user
    response = client.get("/get_token/non_existent_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."
