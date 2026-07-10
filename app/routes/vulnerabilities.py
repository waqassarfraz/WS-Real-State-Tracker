from flask import Blueprint, request, jsonify
from app import db
from app.models import Vulnerability
from app.schemas import vulnerability_schema, vulnerabilities_schema
from marshmallow import ValidationError

vulns_bp = Blueprint('vulnerabilities', __name__, url_prefix='/api/vulnerabilities')

# CREATE
@vulns_bp.route('', methods=['POST'])
def create_vulnerability():
    try:
        vuln = vulnerability_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(vuln)
    db.session.commit()
    return vulnerability_schema.jsonify(vuln), 201

# READ ALL (with search/sort/filter)
@vulns_bp.route('', methods=['GET'])
def get_vulnerabilities():
    query = Vulnerability.query

    search = request.args.get('search')
    if search:
        query = query.filter(Vulnerability.title.ilike(f'%{search}%'))

    severity = request.args.get('severity')
    if severity:
        query = query.filter_by(severity=severity)

    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)

    sort = request.args.get('sort', 'id')
    if sort.startswith('-'):
        query = query.order_by(getattr(Vulnerability, sort[1:]).desc())
    else:
        query = query.order_by(getattr(Vulnerability, sort).asc())

    results = query.all()
    return vulnerabilities_schema.jsonify(results), 200

# READ ONE
@vulns_bp.route('/<int:id>', methods=['GET'])
def get_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if not vuln:
        return jsonify({"error": "Vulnerability not found"}), 404
    return vulnerability_schema.jsonify(vuln), 200

# UPDATE
@vulns_bp.route('/<int:id>', methods=['PUT'])
def update_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if not vuln:
        return jsonify({"error": "Vulnerability not found"}), 404

    try:
        updated = vulnerability_schema.load(request.json, instance=vuln, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.commit()
    return vulnerability_schema.jsonify(updated), 200

# DELETE
@vulns_bp.route('/<int:id>', methods=['DELETE'])
def delete_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if not vuln:
        return jsonify({"error": "Vulnerability not found"}), 404

    if vuln.issues:
        return jsonify({
            "error": "Cannot delete vulnerability with linked issues. Unlink or delete them first."
        }), 400

    db.session.delete(vuln)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 200