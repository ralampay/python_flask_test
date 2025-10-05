# Initialization

1. Create a project

```bash
mkdir project_name
```

2. Target project structure:

```bash
project_name/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── config.py
│
├── tests/
│   └── test_basic.py
│
├── requirements.txt
└── run.py
```

3. Creating a virtual environment

with **`pyenv`**:

```bash
pyenv virtualenv 3.12.3 project_name
pyenv activate project_name
```

with **`venv`**:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

4. Install `flask`:

```bash
pip install flask
```
