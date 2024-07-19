import pytest

from achievement_api.models.achievement import Achievement


@pytest.mark.authenticated("achievements.achievement.delete")
def test_delete_existed(client, dbsessionGen, achievement):
    _achievement = achievement()
    response = client.delete(f"/achievement/{_achievement.id}")
    assert response.status_code == 200
    dbsession = dbsessionGen()
    query = dbsession.query(Achievement).get(_achievement.id)
    assert query is None


@pytest.mark.authenticated("achievements.achievement.delete")
def test_delete_unexisted(client):
    unexisted_id = -1
    response = client.delete(f"/achievement/{unexisted_id}")
    assert response.status_code == 404
