import pytest
from fastapi.testclient import TestClient

from achievement_api.routes.base import app


@pytest.fixture
def client():
    yield TestClient(app)
