from flask import jsonify, request

def json_response(data=None, message=None, status="success", code=200, **kwargs):
    response = {
        "status": status,
        "message": message,
        "data": data
    }

    response.update(kwargs)

    return jsonify(response), code

def authenticate_user():
    token = request.headers.get("Authorization")

    print(f"token: {token}")

    if not token:
        return json_response(
            message="not authenticated",
            status="error",
            code=401
        )
