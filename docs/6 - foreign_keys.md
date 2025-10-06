# Foreign Keys

Let's say you have the following models:

**Owner**
- `id`:`uuid`
- `name`:`string`

**Tower**
- `id`:`uuid`
- `name`:`string`
- `owner_id`:`uuid`

The `owner_id` is referred to as a foreign key to refer to a value in the `id` column (primary key) of an owner.

We would read this as:

- `Owner` has many (can have multiple) towers
- A `Tower` can belong to a single `Owner`.

1. Establish the independent model `Owner`:

```python
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class Owner(db.Model):
    __tablename__ = "owners"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    # Relationship to Tower
    towers = db.relationship('Tower', back_populates='owner', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None

        }

```

2. Establish the dependent model `Tower`:

```python
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from .. import db

class Tower(db.Model):
    __tablename__ = "towers"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    # Foreign key reference to Owner
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('owners.id', ondelete='CASCADE'), nullable=False)

    # Relationship to Owner
    owner = db.relationship('Owner', back_populates='towers')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None

        }
```

## Testing Relationships

Assuming that a `user` has many `load_transactions`.

**Factory Code**:

```python
import factory
import uuid
from app import db
from app.models import User, LoadTransaction

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker("name")

class LoadTransactionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = LoadTransaction
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    id = factory.LazyFunction(uuid.uuid4)
    amount = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    user = factory.SubFactory(UserFactory)
```

**Creating the Test**:

```python
def test_get_user_load_transactions(client, app):
    from tests.factories import UserFactory, LoadTransactionFactory
    from app import db

    with app.app_context():
        # Create a user and 3 load transactions
        user = UserFactory()
        LoadTransactionFactory.create_batch(3, user=user)
        db.session.commit()

        user_id = str(user.id)

    # Act: GET the user's load transactions
    response = client.get(f"/users/{user_id}/load_transactions")

    # Assert
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3

    for tx in data:
        assert "id" in tx
        assert "amount" in tx
```
