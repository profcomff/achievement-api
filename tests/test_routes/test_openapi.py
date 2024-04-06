def test_unprocessable_jsons_no_token(client):
    response = client.get(f"/openapi.json")
    assert response.status_code == 200
