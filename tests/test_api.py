from fastapi.testclient import TestClient
from backend.main import app
def test_health():
    response = TestClient(app).get("/health")
    assert response.status_code == 200 and response.json()["status"] == "ok"
