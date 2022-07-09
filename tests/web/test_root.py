from fastapi.testclient import TestClient

from bakeneko.web import app


def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
