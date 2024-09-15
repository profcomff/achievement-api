import pytest

from achievement_api.models.achievement import Achievement


@pytest.mark.authenticated("achievements.achievement.create", "achievements.achievement.delete")
def test_delete_existed(client, dbsession, achievement_id):
    delete_response = client.delete(f"/achievement/{achievement_id}")
    assert delete_response.status_code == 200
    query = dbsession.get(Achievement, achievement_id)
    assert query is None


@pytest.mark.authenticated("achievements.achievement.delete")
def test_delete_unexisted(client):
    unexisted_id = -1
    response = client.delete(f"/achievement/{unexisted_id}")
    assert response.status_code == 404


@pytest.mark.authenticated("achievements.achievement.create", "achievements.achievement.delete")
def test_get_existed(client, achievement_id):
    response = client.get(f"/achievement/{achievement_id}")
    assert response.status_code == 200
    assert response.json()["id"] == achievement_id


def test_get_unexisted(client):
    unexisted_id = -1
    response = client.get(f"/achievement/{unexisted_id}")
    assert response.status_code == 404


@pytest.mark.authenticated(
    "achievements.achievement.create", "achievements.achievement.edit", "achievements.achievement.delete"
)
def test_edit_existed(client, achievement_id):
    body = {"name": "new name", "description": "new description"}
    response = client.patch(f"/achievement/{achievement_id}", json=body)
    assert response.status_code == 200
    response = client.get(f"/achievement/{achievement_id}")
    assert response.json()["id"] == achievement_id
    assert response.json()["name"] == body["name"]
    assert response.json()["description"] == body["description"]


@pytest.mark.authenticated("achievements.achievement.edit")
def test_edit_unexisted(client):
    body = {"name": "new name", "description": "new description"}
    unexisted_id = -1
    response = client.patch(f"/achievement/{unexisted_id}", json=body)
    assert response.status_code == 404
