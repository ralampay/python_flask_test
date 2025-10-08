from flask import Blueprint
from app.models import User
from app.utils import json_response, authenticate_user

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.before_request
def authenticate():
    return authenticate_user()

@users_bp.route("", methods=["GET"])
def index():
    """Return all users as JSON."""
    users = [u.to_dict() for u in User.query.all()]
    return json_response(data=users, message="All users retrieved")
