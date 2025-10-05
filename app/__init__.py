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
