from flask import Blueprint, jsonify
from app.models import Issue, Vulnerability
from sqlalchemy import func
from app import db

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/summary', methods=['GET'])
def summary():
    issue_status_counts = dict(
        db.session.query(Issue.status, func.count(Issue.id))
        .group_by(Issue.status)
        .all()
    )

    issue_priority_counts = dict(
        db.session.query(Issue.priority, func.count(Issue.id))
        .group_by(Issue.priority)
        .all()
    )

    vuln_status_counts = dict(
        db.session.query(Vulnerability.status, func.count(Vulnerability.id))
        .group_by(Vulnerability.status)
        .all()
    )

    vuln_severity_counts = dict(
        db.session.query(Vulnerability.severity, func.count(Vulnerability.id))
        .group_by(Vulnerability.severity)
        .all()
    )

    return jsonify({
        "issues": {
            "total": Issue.query.count(),
            "by_status": issue_status_counts,
            "by_priority": issue_priority_counts
        },
        "vulnerabilities": {
            "total": Vulnerability.query.count(),
            "by_status": vuln_status_counts,
            "by_severity": vuln_severity_counts
        }
    }), 200