import pytest
from app import create_app, db
from tests.factories import UserFactory

@pytest.fixture(scope="session")
def app():
    app = create_app(env="test")
    app.config["TESTING"] = True

    # Make sure test DB starts clean
    with app.app_context():
        db.drop_all()
        db.create_all()

    yield app

    # Teardown after all tests
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def mock_user(app):
    """Create and persist a fake user in the test DB."""
    with app.app_context():
         # Bind Factory Boy to the active SQLAlchemy session
        UserFactory._meta.sqlalchemy_session = db.session

        user = UserFactory()
        db.session.add(user)
        db.session.commit()

        return user
