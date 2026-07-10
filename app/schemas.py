from app import ma
from app.models import Issue, Vulnerability
from marshmallow import validate

class VulnerabilitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vulnerability
        load_instance = True

    severity = ma.String(validate=validate.OneOf(['low', 'medium', 'high', 'critical']), required=True)
    cvss_score = ma.Float(validate=validate.Range(min=0.0, max=10.0), required=True)
    title = ma.String(validate=validate.Length(min=1, max=200), required=True)
    affected_system = ma.String(required=True)
    status = ma.String(validate=validate.OneOf(['open', 'mitigated', 'accepted_risk', 'closed']))

class IssueSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Issue
        load_instance = True
        include_fk = True

    title = ma.String(validate=validate.Length(min=1, max=200), required=True)
    priority = ma.String(validate=validate.OneOf(['low', 'medium', 'high', 'critical']))
    status = ma.String(validate=validate.OneOf(['open', 'in_progress', 'resolved', 'closed']))

vulnerability_schema = VulnerabilitySchema()
vulnerabilities_schema = VulnerabilitySchema(many=True)
issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)