from conftest import client
import logging


def create_user_helper(username: str, email: str, password: str):
    payload = {"username": username, "email": email, "password": password}
    client.post("/api/auth/signup", json=payload)


def test_returns_error_when_invalid_username():
    payload = {"username": "", "password": "password123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 422


def test_returns_error_when_invalid_password():
    payload = {"username": "test1111", "password": ""}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 422


def test_returns_error_if_user_does_not_exist():
    payload = {"username": "test123123", "password": "testpassword123"}
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 422


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
    payload = {
        "username": dummy_user_data["username"],
        "password": dummy_user_data["password"],
    }
    response = client.post("/api/auth/login", data=payload)
    parsed_response = response.json()
    assert response.status_code == 200

    assert "access_token" in parsed_response
    assert isinstance(parsed_response["access_token"], str)
