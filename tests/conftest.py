import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app(env="test")
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
