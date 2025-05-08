

def test_health_check(client_fixture):
    response = client_fixture.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

