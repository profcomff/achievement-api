import pytest

from achievement_api.models.achievement import Achievement


@pytest.mark.authenticated("achievements.achievement.create", "achievements.achievement.delete")
def test_delete_existed(client, dbsession):
    post_response = client.post("/achievement", json={"name": "test name", "description": "test description"})
    delete_response = client.delete(f"/achievement/{post_response.json()['id']}")
    assert delete_response.status_code == 200
    query = dbsession.get(Achievement, post_response.json()["id"])
    assert query is None


@pytest.mark.authenticated("achievements.achievement.delete")
def test_delete_unexisted(client):
    unexisted_id = -1
    response = client.delete(f"/achievement/{unexisted_id}")
    assert response.status_code == 404
