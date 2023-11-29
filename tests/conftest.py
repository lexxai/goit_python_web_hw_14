from datetime import datetime
import os
from pathlib import Path
import sys
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

curr_path = Path(__file__).resolve().parent
hw_path: str = str(curr_path.parent.joinpath("hw14"))

sys.path.append(hw_path)
# print(f"{hw_path=}", sys.path)
os.environ["PYTHONPATH"] += os.pathsep + hw_path

from main import app, get_limit
from src.database.models import Base
from src.database.db import get_db, get_redis

db_path = curr_path / "test.sqlite"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    class Empty:
        ...

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    async def override_get_limit():
        return None

    async def override_get_redis():
        return None
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_limit] = override_get_limit
    app.dependency_overrides[get_redis] = override_get_redis

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {
        "username": "lexxaiedu",
        "email": "lexxaiedu@example.com",
        "password": "qwerty",
        "avatar": None,
        "role": "user",
    }


@pytest.fixture(scope="module")
def contact():
    result = {
        "first_name": "aaaa",
        "last_name": "bbbbb",
        "email": "aaa@uu.cc",
        "phone": None,
        "birthday": None,
        "comments": None,
        "favorite": False,
        "user_id": 1,
    }
    return result
