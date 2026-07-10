from datetime import datetime
from app import db

class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # low/medium/high/critical
    cvss_score = db.Column(db.Float, nullable=False)
    affected_system = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    issues = db.relationship('Issue', backref='vulnerability', lazy=True)


class Issue(db.Model):
    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='open')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    assignee = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    linked_vulnerability_id = db.Column(db.Integer, db.ForeignKey('vulnerabilities.id'), nullable=True)