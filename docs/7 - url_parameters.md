# URL Parameters

You can pass URL parameters to your route definition:

```python
from flask import Blueprint, jsonify, abort
from app.models import User

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("/<uuid:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify({
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    })
```

Here:
- `uuid` refers to the data type of `user_id`

Possible tests:

**User Not Found**

```python
import uuid

def test_get_user_not_found(client):
    random_id = uuid.uuid4()
    response = client.get(f"/users/{random_id}")
    assert response.status_code == 404
```

**User Found**

```python
def test_get_user_by_id(client, mock_user):
    response = client.get(f"/users/{mock_user.id}")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == str(mock_user.id)
    assert data["name"] == mock_user.name
```

**id parameter is not in uuid format**

Note that in this example, since `abcd` does not resolve to a valid uuid format, flask will treat it as a `404`.

```python
def test_invalid_id(client):
    response = client.get(f"/users/abcd")
    assert response.status_code == 404

```
