# Mock Setup

1. Install dependencies

```bash
pip install faker factory-boy pytest pytest-flask
```

2. Modify `tests/conftest.py`:

```python
import pytest
from app import create_app

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
```

3. Create a factorires configuration in `tests/factories.py` with the necessary mock logic

**Example: `UserFactory`:**

```python
import factory
from faker import Faker
from app.models import User

fake = Faker()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "flush"

    id = factory.Faker("uuid4")
    email = factory.LazyAttribute(lambda _: fake.email())
    encrypted_password = factory.LazyAttribute(lambda _: fake.password(length=10))
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    status = "active"
```

4. Add a `mock_user(app)` fixture in `tests/conftest.py`:

Import:

```python
from tests.factories import UserFactory
```

Add fixture:

```python
@pytest.fixture
def mock_user(app):
    """Create and persist a fake user in the test DB."""
    with app.app_context():
        user = UserFactory()
        db.session.add(user)
        db.session.commit()

        return user
```
