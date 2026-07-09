# Requirements — WS Real Estate Issue & Vulnerability Tracker

## Scenario
WS Real Estate's IT team currently tracks software bugs and security 
vulnerabilities in separate spreadsheets. This system unifies both into 
a single API-driven tracker so nothing is missed.

## Functional Requirements
- Create, view, update, delete Issues
- Create, view, update, delete Vulnerabilities
- Search issues/vulnerabilities by keyword
- Filter by status, severity, priority
- Sort by date created, severity, priority
- Reporting: count of open items by severity/status
- Input validation on all create/update operations
- Data integrity: no orphaned linked records

## Data Model

### Issue
| Field | Type | Rules |
|---|---|---|
| id | int (PK) | auto-generated |
| title | string | required, max 200 chars |
| description | text | required |
| status | enum | open / in_progress / resolved / closed |
| priority | enum | low / medium / high / critical |
| assignee | string | optional |
| created_at | datetime | auto |
| updated_at | datetime | auto |
| linked_vulnerability_id | int (FK, nullable) | must reference existing vulnerability |

### Vulnerability
| Field | Type | Rules |
|---|---|---|
| id | int (PK) | auto-generated |
| title | string | required |
| description | text | required |
| severity | enum | low / medium / high / critical |
| cvss_score | float | required, 0.0–10.0 |
| affected_system | string | required |
| status | enum | open / mitigated / accepted_risk / closed |
| discovered_at | datetime | required |
| resolved_at | datetime | optional |

## Non-functional requirements
- RESTful JSON API built with Flask
- Proper HTTP status codes (200/201/400/404/500)
- Automated tests (pytest)
- Postman collection for manual testing