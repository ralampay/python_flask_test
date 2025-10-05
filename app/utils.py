from flask import jsonify

def json_response(data=None, message=None, status="success", code=200, **kwargs):
    response = {
        "status": status,
        "message": message,
        "data": data
    }

    response.update(kwargs)

    return jsonify(response), code
