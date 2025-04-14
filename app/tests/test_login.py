from conftest import client
import logging


def create_user_helper(username: str, email: str, password: str):
    payload = {"username": username, "email": email, "password": password}
    client.post("/api/auth/signup", json=payload)


def test_returns_error_when_invalid_email():
    payload = {"email": "", "password": "password123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 422


def test_returns_error_when_invalid_password():
    payload = {"email": "test@email.com", "password": ""}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 422


def test_returns_error_if_user_does_not_exist():
    payload = {"email": "test@email.com", "password": "testpassword123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 404


def test_returns_token_and_user_when_payload_valid():
    dummy_user_data = {
        "username": "testuser",
        "email": "test@mail.com",
        "password": "testpassword123",
    }
    create_user_helper(
        username=dummy_user_data["username"],
        email=dummy_user_data["email"],
        password=dummy_user_data["password"],
    )
    payload = {"email": "test@mail.com", "password": "testpassword123"}
    response = client.post("/api/auth/login", json=payload)
    parsed_response = response.json()
    assert response.status_code == 200

    assert "token" in parsed_response
    assert isinstance(parsed_response["token"], str)
    assert "user" in parsed_response
    assert isinstance(parsed_response["user"], dict)

    user_data = parsed_response["user"]
    assert "id" in user_data
    assert isinstance(user_data["id"], int)

    assert "email" in user_data
    assert isinstance(user_data["email"], str)
    assert user_data["email"] == dummy_user_data["email"]

    assert "username" in user_data
    assert isinstance(user_data["username"], str)
    assert user_data["username"] == dummy_user_data["username"]
