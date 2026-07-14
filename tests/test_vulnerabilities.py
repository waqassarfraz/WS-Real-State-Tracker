import pytest
from app import create_app, db


@pytest.fixture
def client():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_vulnerability(client):
    response = client.post('/api/vulnerabilities', json={
        "title": "Test Vulnerability",
        "description": "A test vulnerability for automated testing",
        "severity": "high",
        "cvss_score": 7.5,
        "affected_system": "test-system",
        "status": "open"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Vulnerability"
    assert data["severity"] == "high"


def test_reject_invalid_cvss_score(client):
    response = client.post('/api/vulnerabilities', json={
        "title": "Bad Vulnerability",
        "description": "CVSS score out of range",
        "severity": "high",
        "cvss_score": 15.0,
        "affected_system": "test-system"
    })
    assert response.status_code == 400


def test_reject_invalid_severity(client):
    response = client.post('/api/vulnerabilities', json={
        "title": "Bad Severity",
        "description": "Invalid severity value",
        "severity": "super-critical",
        "cvss_score": 5.0,
        "affected_system": "test-system"
    })
    assert response.status_code == 400


def test_get_all_vulnerabilities(client):
    client.post('/api/vulnerabilities', json={
        "title": "Vuln 1",
        "description": "First test vulnerability",
        "severity": "low",
        "cvss_score": 2.0,
        "affected_system": "system-a"
    })
    response = client.get('/api/vulnerabilities')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


def test_get_single_vulnerability_not_found(client):
    response = client.get('/api/vulnerabilities/999')
    assert response.status_code == 404


def test_update_vulnerability(client):
    create_response = client.post('/api/vulnerabilities', json={
        "title": "Original Title",
        "description": "Will be updated",
        "severity": "medium",
        "cvss_score": 5.0,
        "affected_system": "system-b"
    })
    vuln_id = create_response.get_json()["id"]

    update_response = client.put(f'/api/vulnerabilities/{vuln_id}', json={
        "status": "mitigated"
    })
    assert update_response.status_code == 200
    assert update_response.get_json()["status"] == "mitigated"


def test_delete_vulnerability(client):
    create_response = client.post('/api/vulnerabilities', json={
        "title": "To Be Deleted",
        "description": "This will be removed",
        "severity": "low",
        "cvss_score": 1.0,
        "affected_system": "system-c"
    })
    vuln_id = create_response.get_json()["id"]

    delete_response = client.delete(f'/api/vulnerabilities/{vuln_id}')
    assert delete_response.status_code == 200

    get_response = client.get(f'/api/vulnerabilities/{vuln_id}')
    assert get_response.status_code == 404