import os
import yaml
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.utils import json_response

# --- Initialize extensions (but not bind yet) ---
db = SQLAlchemy()
migrate = Migrate()

def create_app(env=None):
    app = Flask(__name__)

    # enable CORS for all routes
    CORS(app)

    # --- Load database config ---
    config_path = os.path.join(os.path.dirname(__file__), "config", "database.yml")
    with open(config_path, "r") as f:
        db_configs = yaml.safe_load(f)

    # Choose environment
    env = env or os.getenv("FLASK_ENV", "development")
    db_uri = db_configs[env]["uri"]
    # --- Fix relative SQLite paths ---
    if db_uri.startswith("sqlite:///"):
        # Remove 'sqlite:///' prefix to get relative file path
        relative_path = db_uri.replace("sqlite:///", "")
        # Resolve absolute path relative to the Flask app root
        abs_path = os.path.join(app.root_path, "..", relative_path)
        # Ensure the directory exists
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        # Rebuild full absolute URI
        db_uri = f"sqlite:///{abs_path}"

    print("Using database:", db_uri)  # ✅ confirm full absolute path

     # --- Apply configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Initialize extensions ---
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models *after* db.init_app so migrations detect them
    from .models import User
    from .routes import api
    from .controllers.users_controller import users_bp

    app.register_blueprint(api)
    app.register_blueprint(users_bp)

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
