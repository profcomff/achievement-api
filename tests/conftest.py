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
def achievement(dbsession):
    name = "Test achievement"
    owner_id = 1
    achievement = Achievement(name=name, description="", owner_user_id=owner_id)
    dbsession.add(achievement)
    dbsession.commit()
    yield achievement
