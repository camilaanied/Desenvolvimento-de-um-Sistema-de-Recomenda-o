from fastapi.testclient import TestClient
from recomendador.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "API do Sistema de Recomendação" in data["message"]


def test_recommend_endpoint():
    response = client.get("/recommend/1?k=5")
    assert response.status_code == 200
    data = response.json()

    assert "user_id" in data
    assert data["user_id"] == 1
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
