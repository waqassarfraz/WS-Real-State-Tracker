from flask import Blueprint, request, jsonify
from app import db
from app.models import Issue, Vulnerability
from app.schemas import issue_schema, issues_schema
from marshmallow import ValidationError

issues_bp = Blueprint('issues', __name__, url_prefix='/api/issues')

# CREATE
@issues_bp.route('', methods=['POST'])
def create_issue():
    data = request.json

    linked_id = data.get('linked_vulnerability_id')
    if linked_id:
        vuln = Vulnerability.query.get(linked_id)
        if not vuln:
            return jsonify({"errors": {"linked_vulnerability_id": ["No vulnerability with this id exists"]}}), 400

    try:
        issue = issue_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(issue)
    db.session.commit()
    return issue_schema.jsonify(issue), 201

# READ ALL (with search/sort/filter)
@issues_bp.route('', methods=['GET'])
def get_issues():
    query = Issue.query

    search = request.args.get('search')
    if search:
        query = query.filter(Issue.title.ilike(f'%{search}%'))

    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)

    priority = request.args.get('priority')
    if priority:
        query = query.filter_by(priority=priority)

    sort = request.args.get('sort', 'id')
    if sort.startswith('-'):
        query = query.order_by(getattr(Issue, sort[1:]).desc())
    else:
        query = query.order_by(getattr(Issue, sort).asc())

    results = query.all()
    return issues_schema.jsonify(results), 200

# READ ONE
@issues_bp.route('/<int:id>', methods=['GET'])
def get_issue(id):
    issue = Issue.query.get(id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404
    return issue_schema.jsonify(issue), 200

# UPDATE
@issues_bp.route('/<int:id>', methods=['PUT'])
def update_issue(id):
    issue = Issue.query.get(id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    try:
        updated = issue_schema.load(request.json, instance=issue, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.commit()
    return issue_schema.jsonify(updated), 200

# DELETE
@issues_bp.route('/<int:id>', methods=['DELETE'])
def delete_issue(id):
    issue = Issue.query.get(id)
    if not issue:
        return jsonify({"error": "Issue not found"}), 404

    db.session.delete(issue)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200