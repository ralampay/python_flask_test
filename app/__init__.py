import os
import yaml
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes import api
from app.utils import json_response

db = SQLAlchemy()
migrate = Migrate()

def create_app(env=None):
    app = Flask(__name__)

    # enable CORS for all routes
    CORS(app)

    app.register_blueprint(api)

    # --- Load database config ---
    config_path = os.path.join(os.path.dirname(__file__), "config", "database.yml")
    with open(config_path, "r") as f:
        db_configs = yaml.safe_load(f)

    # Choose environment
    env = env or os.getenv("FLASK_ENV", "development")
    db_uri = db_configs[env]["uri"]

     # --- Apply configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Initialize extensions ---
    db.init_app(app)
    migrate.init_app(app, db)

    # Error handler: 404
    @app.errorhandler(404)
    def not_found(e):
        return json_response(
            status="error",
            message="not found",
            code=404
        )

    # Error handler: 500
    @app.errorhandler(500)
    def internal_error(e):
        return json_response(
            status="error",
            message="internal server error",
            code=500
        )

    return app
