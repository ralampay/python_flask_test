from flask import Blueprint, jsonify, request

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "hello world!"
    })

@api.route("/echo", methods=["POST"])
def echo():
    data = request.get_json()

    return jsonify({
        "status": "success",
        "received": data
    }), 200
