# PyTest Integration

1. Configure a `client` to invoke without running the server:

In `tests/conftest.py`:

```python
import os
import sys
import pytest

# Add the project root directory (where run.py and app/ live) to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
```

2. Write tests for routes:

In `tests/test_routes.py`:

```python
def test_home_route(client):
    """Test the GET / route"""
    response = client.get("/")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["message"] == "Welcome to Flask JSON API"


def test_echo_route(client):
    """Test the POST /echo route"""
    payload = {"name": "Raphael"}
    response = client.post("/echo", json=payload)
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "success"
    assert json_data["data"] == payload


def test_404_route(client):
    """Test non-existent route returns JSON 404"""
    response = client.get("/doesnotexist")
    json_data = response.get_json()

    assert response.status_code == 404
    assert json_data["status"] == "error"
    assert json_data["message"] == "Not Found"
```

3. Run the tests:

```bash
pytest -v
```

## Cleaner with `pytest.ini`

1. Create a file `pytest.ini` at project root:

```
[pytest]
testpaths = tests
pythonpath = .
```
