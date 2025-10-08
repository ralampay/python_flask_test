# Authentication

You could have an authentication method that implements the logic of fetching a user based on a given token (usually passed through the header):

```python
def authenticate_user():
    token = request.headers.get("Authorization")

    if not token:
        return json_response(
            message="not authenticated",
            status="error",
            code=401
        )
```

To attach this to a controller route defined by a blueprint, we can create a method and annotate it with `@your_blueprint.before_request`. For example:

```python
@users_bp.before_request
def authenticate_routes():
    return authenticate_user() 
```
