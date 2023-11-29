from datetime import datetime
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

hw_path: str = str(Path(__file__).resolve().parent.parent.joinpath("hw14"))
os.environ["PATH"] += os.pathsep + hw_path
os.environ["PYTHONPATH"] += os.pathsep + hw_path

from src.database.models import Contact, User
from src.shemas.contact import ContactModel

# from src.services.auth.auth import auth_service
from src.database import db


class MockRedis:
    async def get_connection(self, *args):
        print("MockRedis get_connection")
        return False

    async def get(self, *args):
        print("MockRedis get")
        return True

    async def set(self, *args):
        print("MockRedis set")
        return True

    async def expire(self, *args):
        print("MockRedis expire")
        return True

    async def release(self, *args):
        print("MockRedis release")
        return True


def create_user(client, session, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    # assert response.status_code == 201, response.text
    # data = response.json()
    # assert data["user"]["email"] == user.get("email")
    # assert "id" in data["user"]


def get_access_token_user(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    access_token = data["access_token"]
    return f"Bearer {access_token}"


@pytest.fixture()
def token(client, user, session, monkeypatch):
    # print(f"token {db.redis_pool=}")
    create_user(client, session, user, monkeypatch)
    return get_access_token_user(client, user)


def s_test_create_contact_0(client, contact, token):
    with patch("src.database.db.redis_pool", False):
        headers = {"Authorization": token}
        response = client.post("/api/contacts", headers=headers, json=contact)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == contact.get("first_name")
        assert "id" in data


# @patch("src.database.db.get_redis", gr)


# @patch("src.database.db.redis_pool", False)
def test_create_contact(client, contact, token):
    # db.redis_pool = MagicMock(spec=MockRedis)
    # SUPPRESS REDIS CONNECTION POOL  !!! is  redis_pool
    # with patch("src.database.db.redis_pool", False):
    response = client.post("/api/contacts", json=contact, headers={"Authorization": token})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == contact.get("first_name")
    assert "id" in data


# @patch("src.database.db.redis_pool", False)
def test_get_contact(client, token, contact):
    # with patch("src.database.db.redis_pool", False):
    response = client.get("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == contact.get("first_name")
    assert "id" in data


# @patch("src.database.db.redis_pool", False)
def test_get_contact_not_found(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.get("/api/contacts/2", headers={"Authorization": token})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not found"


# @patch("src.database.db.redis_pool", False)
def test_get_contacts(client, contact, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.get("/api/contacts", headers={"Authorization": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["first_name"] == contact.get("first_name")
    assert "id" in data[0]


# @patch("src.database.db.redis_pool", False)
def test_update_contact(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.put("/api/contacts/1", json={"email": "new@email.com"}, headers={"Authorization": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "new@email.com"
    assert "id" in data


# @patch("src.database.db.redis_pool", False)
def test_update_contact_not_found(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.put("/api/contacts/2", json={"email": "new@email.com"}, headers={"Authorization": token})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not found"


# @patch("src.database.db.redis_pool", False)
def test_delete_contact(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.delete("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 204, response.text
    # data = response.json()
    # assert data["email"] == "new@email.com"
    # assert "id" in data


# @patch("src.database.db.redis_pool", False)
def test_repeat_delete_contact(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.delete("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not found"
