from conftest import client
import logging


def test_returns_error_when_invalid_email():
    payload = {
        "email": "aaaaa",
        "password": "123",
        "username": "test username",
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 422


def test_returns_error_when_invalid_password():
    payload = {
        "email": "aaaaa",
        "password": "",
        "username": "test username",
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 422


def test_returns_error_when_invalid_username():
    payload = {
        "email": "test@email.com",
        "password": "testpassword",
        "username": "",
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 422


def test_creates_user_when_params_valid():
    payload = {
        "email": "test@email.com",
        "password": "password123",
        "username": "test username",
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 201
