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

@pytest.fixture(scope="session")
def session(app):
    with app.app_context():
        yield db.session

@pytest.fixture
def mock_user(session):
    #  Bind Factory Boy to this active SQLAlchemy session
    UserFactory._meta.sqlalchemy_session = session

    user = UserFactory()
    session.add(user)
    session.commit()

    return user
