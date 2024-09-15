import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from achievement_api.models.achievement import Achievement
from achievement_api.routes.base import app
from achievement_api.settings import get_settings


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture(scope='session')
def dbsession():
    settings = get_settings()
    engine = create_engine(str(settings.DB_DSN))
    TestingSessionLocal = sessionmaker(bind=engine)
    yield TestingSessionLocal()


@pytest.fixture
def achievement_id(client, dbsession):
    post_response = client.post("/achievement", json={"name": "test name", "description": "test description"})
    id = post_response.json()["id"]
    yield id
    if dbsession.get(Achievement, id):
        client.delete(f"/achievement/{id}")
