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


def test_create_issue(client):
    response = client.post('/api/issues', json={
        "title": "Test Issue",
        "description": "A test issue for automated testing",
        "status": "open",
        "priority": "medium",
        "assignee": "Tester"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test Issue"
    assert data["priority"] == "medium"


def test_reject_invalid_priority(client):
    response = client.post('/api/issues', json={
        "title": "Bad Priority Issue",
        "description": "Invalid priority value",
        "priority": "super-urgent"
    })
    assert response.status_code == 400


def test_reject_missing_title(client):
    response = client.post('/api/issues', json={
        "description": "No title provided"
    })
    assert response.status_code == 400


def test_get_all_issues(client):
    client.post('/api/issues', json={
        "title": "Issue 1",
        "description": "First test issue"
    })
    response = client.get('/api/issues')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


def test_update_issue(client):
    create_response = client.post('/api/issues', json={
        "title": "Original Issue",
        "description": "Will be updated"
    })
    issue_id = create_response.get_json()["id"]

    update_response = client.put(f'/api/issues/{issue_id}', json={
        "status": "resolved"
    })
    assert update_response.status_code == 200
    assert update_response.get_json()["status"] == "resolved"


def test_delete_issue(client):
    create_response = client.post('/api/issues', json={
        "title": "To Be Deleted",
        "description": "This will be removed"
    })
    issue_id = create_response.get_json()["id"]

    delete_response = client.delete(f'/api/issues/{issue_id}')
    assert delete_response.status_code == 200

    get_response = client.get(f'/api/issues/{issue_id}')
    assert get_response.status_code == 404


def test_link_issue_to_invalid_vulnerability(client):
    response = client.post('/api/issues', json={
        "title": "Linked Issue",
        "description": "References a vulnerability that does not exist",
        "linked_vulnerability_id": 999
    })
    assert response.status_code == 400


def test_cannot_delete_vulnerability_with_linked_issue(client):
    vuln_response = client.post('/api/vulnerabilities', json={
        "title": "Linked Vulnerability",
        "description": "Has a linked issue",
        "severity": "high",
        "cvss_score": 8.0,
        "affected_system": "system-x"
    })
    vuln_id = vuln_response.get_json()["id"]

    client.post('/api/issues', json={
        "title": "Dependent Issue",
        "description": "Linked to the vulnerability above",
        "linked_vulnerability_id": vuln_id
    })

    delete_response = client.delete(f'/api/vulnerabilities/{vuln_id}')
    assert delete_response.status_code == 400