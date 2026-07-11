from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)
    from app.routes.issues import issues_bp
    from app.routes.vulnerabilities import vulns_bp
    from app.routes.reports import reports_bp
    app.register_blueprint(issues_bp)
    app.register_blueprint(vulns_bp)
    app.register_blueprint(reports_bp)

    with app.app_context():
        db.create_all()

    return app