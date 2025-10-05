from flask import Flask
from flask_cors import CORS
from .routes import api

def create_app():
    app = Flask(__name__)

    # enable CORS for all routes
    CORS(app)

    app.register_blueprint(api)

    # Error handler: 404
    @app.errorhandler(404)
    def not_found(e):
        return {
            "error": "Not found",
            "message": str(e)
        }, 404

    return app
