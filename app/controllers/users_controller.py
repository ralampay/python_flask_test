from flask import Blueprint
from app.models import User
from app.utils import json_response

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("", methods=["GET"])
def index():
    """Return all users as JSON."""
    users = [u.to_dict() for u in User.query.all()]
    return json_response(data=users, message="All users retrieved")
