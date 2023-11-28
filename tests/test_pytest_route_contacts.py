from datetime import datetime
import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest

hw_path: str = str(Path(__file__).resolve().parent.parent.joinpath("hw14"))
os.environ["PATH"] += os.pathsep + hw_path
os.environ["PYTHONPATH"] += os.pathsep + hw_path

from src.database.models import Contact, User
from src.shemas.contact import ContactModel


def test_create_user(client, session, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)
    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.get("email")
    assert "id" in data["user"]


def get_access_token_user(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    access_token = data["access_token"]
    return f"Bearer {access_token}"


def test_create_contact(client, contact, user ):
    access_token = get_access_token_user(client, user)
    headers = {
        "Authorization": access_token
    }
    response = client.post("/api/contacts", headers=headers,  json=contact )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == contact.get("first_name")
    assert "id" in data
