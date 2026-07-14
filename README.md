# WS Real Estate — Issue & Vulnerability Tracker

An API-based issue and vulnerability tracking system built for **WS Real Estate**, 
developed as part of an Advanced Programming CA.

## Overview

WS Real Estate's IT team currently tracks software bugs and security vulnerabilities 
across separate spreadsheets, leading to duplicated effort and missed issues. This 
system unifies both into a single RESTful API so nothing falls through the cracks. 
Issues can optionally be linked to a Vulnerability, allowing the team to trace 
software problems back to their root security cause.

## Tech Stack

- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-Marshmallow
- **Database:** SQLite
- **Testing:** Pytest, Postman
- **Validation:** Marshmallow schemas

## Setup Instructions

1. Clone the repository:
`git clone https://github.com/waqassarfraz/WS-Real-State-Tracker.git`
2. Create and activate a virtual environment:
`python -m venv venv` then `venv\Scripts\activate`
3. Install dependencies:
`pip install -r requirements.txt`
4. Run the application:
`python run.py`
5. The API will be available at `http://127.0.0.1:5000`

## Running Tests
All 8 automated tests should pass, covering CRUD operations, validation rules, 
and data integrity constraints.

## API Endpoints

### Vulnerabilities

- POST `/api/vulnerabilities` — Create a new vulnerability
- GET `/api/vulnerabilities` — List all (supports `?search=`, `?severity=`, `?status=`, `?sort=`)
- GET `/api/vulnerabilities/<id>` — Get a single vulnerability
- PUT `/api/vulnerabilities/<id>` — Update a vulnerability
- DELETE `/api/vulnerabilities/<id>` — Delete (blocked if linked issues exist)

### Issues

- POST `/api/issues` — Create a new issue (optionally with `linked_vulnerability_id`)
- GET `/api/issues` — List all (supports `?search=`, `?priority=`, `?status=`, `?sort=`)
- GET `/api/issues/<id>` — Get a single issue
- PUT `/api/issues/<id>` — Update an issue
- DELETE `/api/issues/<id>` — Delete an issue

### Reports

- GET `/api/reports/summary` — Counts of issues/vulnerabilities by status, priority, and severity

## Data Model

See `docs/requirements.md` for full field-level requirements, validation rules, and the data model.

**Vulnerability:** title, description, severity (low/medium/high/critical), cvss_score (0.0–10.0), affected_system, status, discovered_at, resolved_at

**Issue:** title, description, status, priority (low/medium/high/critical), assignee, created_at, updated_at, linked_vulnerability_id (optional)

## Key Features

- Full CRUD for both Issues and Vulnerabilities
- Input validation (required fields, enum constraints, CVSS range checks) via Marshmallow
- Search by keyword, filter by status/severity/priority, sort ascending/descending
- Referential integrity: a Vulnerability cannot be deleted while Issues are linked to it
- Reporting endpoint summarizing open items by category
- Automated test suite (pytest) and manual Postman test collection

## Testing Evidence

- `postman_collection.json` — importable collection of 13 requests covering every endpoint, including deliberate invalid-data requests used to verify validation
- `tests/` — automated pytest suite, 8 tests, all passing

## Code Attribution Summary

This project was developed by the author with step-by-step guidance from Claude 
(Anthropic AI assistant), used throughout for explaining concepts, structuring the 
codebase, generating code to type in, and debugging errors as they occurred. 
No pre-existing project, template, or another person's codebase was copied wholesale.

| Commit(s) | Description | Source |
|---|---|---|
| All commits | Application code (models, routes, schemas, tests), configuration, and documentation | Self, typed and committed by the author, with structure and code suggested step-by-step by Claude (AI-assisted) and reviewed/understood by the author before committing |

Commit messages in this repository use the `[self]` tag to indicate the author 
personally wrote, tested, and committed each change. This README note clarifies 
that AI assistance (Claude) was used as a guided-learning tool throughout the 
development process, consistent with the assignment's requirement to attribute 
AI assistance where used.
