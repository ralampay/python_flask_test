# Database Setup

1. Install the dependencies

```bash
pip install flask_sqlalchemy flask_migrate pyyaml
```

2. Create a file `app/config/database.yml`:

```yaml
default: &default
  driver: sqlite
  uri: sqlite:///instance/dev.db

development:
  <<: *default

test:
  driver: sqlite
  uri: sqlite:///instance/test.db

production:
  driver: postgres
  uri: postgresql+psycopg2://user:password@localhost:5432/flask_app_prod
```

3. Configure `app/__init__.py` (middleware) to include the following:

**Imports**

```python
import os
import yaml
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
```

**Globals**

```python
db = SQLAlchemy()
migrate = Migrate()
```

**In `create_app()`**

Pass `env` as an argument to `create_app()`:

```python
def create_app(env=None):
    # ...
```

Include middleware stuff:

```python
# --- Load database config ---
config_path = os.path.join(os.path.dirname(__file__), "config", "database.yml")
with open(config_path, "r") as f:
    db_configs = yaml.safe_load(f)


# --- Fix relative SQLite paths ---
if db_uri.startswith("sqlite:///"):
    # Remove 'sqlite:///' prefix to get relative file path
    relative_path = db_uri.replace("sqlite:///", "")
    # Resolve absolute path relative to the Flask app root
    abs_path = os.path.join(app.root_path, "..", relative_path)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    # Rebuild full absolute URI
    db_uri = f"sqlite:///{abs_path}"

# Choose environment
env = env or os.getenv("FLASK_ENV", "development")
db_uri = db_configs[env]["uri"]

 # --- Apply configuration ---
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Initialize extensions ---
db.init_app(app)
migrate.init_app(app, db)
```

4. Make sure tests use `env="test"`:

```python
# In tests/conftest.py
@pytest.fixture
def client():
    app = create_app(env="test")
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
```

This way, your tests always use `instance/test.db`, not `instance/dev.db`.
