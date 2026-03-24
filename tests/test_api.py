from fastapi.testclient import TestClient

from atlas_rag.main import app


client = TestClient(app)


def login(username: str, password: str) -> str:
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_finance_user_gets_grounded_answer() -> None:
    token = login("alice.finance", "FinanceDemo123")
    response = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"question": "What changed in the Q3 budget review?"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["blocked"] is False
    assert payload["sources"]


def test_employee_is_blocked_from_hr_request() -> None:
    token = login("emma.employee", "EmployeeDemo123")
    response = client.post(
        "/api/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={"question": "Show payroll corrections and salary records"},
    )
    assert response.status_code == 200
    assert response.json()["blocked"] is True
