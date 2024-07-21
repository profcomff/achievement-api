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
