from conftest import (
    client,
    override_get_unauthenticated_user,
    override_get_authenticated_user,
)
from main import app
from utils import get_current_user


def test_unauthenticated_get():
    app.dependency_overrides[get_current_user] = override_get_unauthenticated_user
    response = client.get("/api/categories")
    assert response.status_code == 401


def test_unauthenticated_post():
    app.dependency_overrides[get_current_user] = override_get_unauthenticated_user
    response = client.post("/api/categories")
    assert response.status_code == 401


def test_unauthenticated_delete():
    app.dependency_overrides[get_current_user] = override_get_unauthenticated_user
    response = client.delete("/api/categories/1")
    assert response.status_code == 401


def test_get():
    app.dependency_overrides[get_current_user] = override_get_authenticated_user
    response = client.get("/api/categories")

    assert response.status_code == 200


def test_post():
    app.dependency_overrides[get_current_user] = override_get_authenticated_user
    payload = {"name": "test1"}
    response = client.post("/api/categories", json=payload)

    assert response.status_code == 201


def test_delete():
    app.dependency_overrides[get_current_user] = override_get_authenticated_user
    payload = {"name": "test1"}
    create_response = client.post("/api/categories", json=payload)
    created_cat = create_response.json()

    delete_response = client.delete(f"/api/categories/{created_cat['id']}")

    assert delete_response.status_code == 200
