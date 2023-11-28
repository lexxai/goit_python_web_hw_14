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
#from src.services.auth.auth import auth_service
from src.database import db


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
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


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
    create_user(client, session, user, monkeypatch)
    return get_access_token_user(client, user)


def s_test_create_contact_0(client, contact, token):
    with patch.object(db, 'redis_pool') as r_mock:
        r_mock.get.return_value = None
        headers = {"Authorization": token}
        response = client.post("/api/contacts", headers=headers, json=contact)
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == contact.get("first_name")
        assert "id" in data


def test_create_contact(client, contact, token):
    # SUPPRESS REDIS CONNECTION POOL  !!! is  redis_pool
    with patch.object(db, 'redis_pool') as r_mock:
        r_mock.get.return_value = None
        response = client.post(
            "/api/contacts",
            json=contact,
            headers={"Authorization": token}
        )
        assert response.status_code == 201, response.text
        data = response.json()
        assert data["first_name"] == contact.get("first_name")
        assert "id" in data
