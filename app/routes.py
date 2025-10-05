from flask import Blueprint, jsonify, request
from .utils import json_response

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def home():
    return json_response(
        message="hello world!"
    )

@api.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()

    return json_response(
        data=data,
        message="echo successful"
    )
