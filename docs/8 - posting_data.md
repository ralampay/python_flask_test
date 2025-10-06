# Posting Data

Example test for creating a user:

```python
def test_create_user_success(client, app):
    payload = {"name": "Raphael Alampay"}

    response = client.post("/users", json=payload)

    # Response checks
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Raphael Alampay"

    # Database checks
    from app.models import User
    from app import db

    with app.app_context():
        user = User.query.filter_by(name="Raphael Alampay").first()
        assert user is not None
        assert str(user.id) == data["id"]
```

Passing the test:

```python
from flask import Blueprint, jsonify, request, abort
from app.models import User
from app import db

bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", methods=["POST"])
def create_user():
    data = request.get_json() or {}

    name = data.get("name")
    if not name:
        abort(400, description="Missing 'name' field")

    user = User(name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": str(user.id),
        "name": user.name,
    }), 201
```

- We get data assumed to posted as a json body using `request.get_json()`
- `data` will now be a dictionary to which we can fetch keys from
