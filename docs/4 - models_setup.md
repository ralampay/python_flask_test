# Models Setup

Create models and perform migrations to update the database schema.

1. Establish a `models` directory where each model configuration will live in:

```bash
python_flask_test/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   ├── config/
│   │   └── database.yml
│   └── models/
│       ├── __init__.py
│       └── user.py
│
├── migrations/
├── instance/
├── run.py
└── requirements.txt
```

2. Inside the `app/models/__init__.py`, create the necessary imports:

```python
from .. import db

# Import individual models here
from .user import User

__all__ = ["User"]
```

3. Create a `User` model in `app/models/user.py`:

```python
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from .. import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    email = db.Column(db.String(255), nullable=False, unique=True)
    encrypted_password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow,
                           nullable=False)

    def to_dict(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
```

4. Update app initialization to include the models:

```python
# Import models *after* db.init_app so migrations detect them
from .models import User
```

5. Workflow for making database changes:

```bash
# Ensure environment
export FLASK_APP=run.py
export FLASK_ENV=development

# Initialize migrations folder
flask db init

# Create initial migration based on current models
flask db migrate -m "Initial schema"

# Apply migration → creates dev.db and tables
flask db upgrade
```
