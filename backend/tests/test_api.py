from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_records_endpoint():
    r = client.get("/crawl/records")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_run_endpoint():
    r = client.post("/crawl/run")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "job_id" in data