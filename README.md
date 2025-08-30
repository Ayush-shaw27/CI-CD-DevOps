# Medical Records API - DevSecOps Backend

A secure medical records management system built with FastAPI, SQLAlchemy, and JWT auth, with DevSecOps integration for CI/CD secret scanning.

## Project Structure

```
CI-CD-DevOps/
├── api/
│   ├── auth.py               # Authentication endpoints
│   ├── patients.py           # Patient CRUD endpoints
│   └── schemas.py            # Pydantic models (v2 compatible)
├── auth/
│   ├── dependencies.py       # Auth dependencies (JWT Bearer)
│   └── security.py           # JWT and password utilities
├── database/
│   ├── models.py             # SQLAlchemy models and DB session
│   └── seed_data.py          # Seed initial users and patients
├── scanner/
│   ├── __init__.py
│   └── gitleaks_scanner.py   # GitLeaks integration wrapper
├── scripts/
│   └── run_security_scan.py  # Entry point for security scans
├── tests/
│   ├── test_api.py           # API endpoint tests
│   ├── test_scanner.py       # Scanner tests
│   └── test_database_models.py # DB env and connection tests
├── reports/                  # Generated scan reports (created at runtime)
├── main.py                   # FastAPI app (lifespan used for seeding)
├── requirements.txt          # Python dependencies
└── .env.example              # Example environment configuration
```

## Requirements

- Python 3.10+
- MySQL 8.x (or compatible)
- Pip and virtual environment
- Optional: GitLeaks installed on the system PATH for security scanning

## Setup

1) Clone the repository

```
git clone <repo-url>
cd CI-CD-DevOps
```

2) Create and activate a virtual environment

```
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

3) Install dependencies

```
pip install -r requirements.txt
```

4) Configure environment

Copy .env.example to .env and edit values as needed.

```
cp .env.example .env   # Windows: copy .env.example .env
```

Required variables:
- DATABASE_URL (mysql+pymysql://user:pass@host:port/db)
- SECRET_KEY (JWT secret)
- ACCESS_TOKEN_EXPIRE_MINUTES (default 30)
- CORS_ORIGINS (comma-separated list)
- Optional: TEST_DATABASE_URL for running API tests against a test DB

5) Prepare MySQL

Create databases for development and testing.

```
mysql -u root -p
CREATE DATABASE medical_records;
CREATE DATABASE medical_records_test;
GRANT ALL PRIVILEGES ON medical_records.* TO 'root'@'localhost';
GRANT ALL PRIVILEGES ON medical_records_test.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

6) Initialize and seed the database

Option A: Use the seed script (creates tables and inserts initial data)

```
python database/seed_data.py
```

Option B: Create tables only

```
python -c "from database.models import create_tables; create_tables()"
```

## Running the Application

Development (auto-reload via uvicorn is already wired if you prefer):

```
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at http://localhost:8000

API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

- JWT-based authentication
- Default seeded users (if you ran the seeder):
  - Doctor: username=dr_smith, password=doctor123
  - Staff: username=nurse_jane, password=staff123

Login flow:
1) POST /auth/login with JSON body {"username": "...", "password": "..."}
2) Receive access_token in response
3) Include header Authorization: Bearer <access_token> for protected routes

## API Endpoints

Authentication
- POST /auth/login
- POST /auth/register

Patients (requires Authorization header)
- GET /patients/
- GET /patients/{id}
- POST /patients/
- PUT /patients/{id}
- DELETE /patients/{id}

System
- GET /
- GET /health

## Configuration Notes

- .env is loaded from the project root regardless of current working directory
- SECRET_KEY and ACCESS_TOKEN_EXPIRE_MINUTES are read from environment variables
- CORS_ORIGINS can be set via environment (comma-separated)
- SQLAlchemy version is 1.4.x for compatibility across environments
- Pydantic models are v2-compatible

## Testing

Prerequisites:
- Ensure MySQL test database exists: medical_records_test
- Set TEST_DATABASE_URL in environment or rely on default inside tests if configured

Run tests:

```
pytest -q
```

Notes:
- Some tests will be skipped automatically if the MySQL test database is not available
- tests/test_database_models.py includes a connectivity helper test without hitting a live DB by mocking the engine

## DevSecOps: Security Scanning

Manual security scan (requires GitLeaks installed on your system PATH):

```
python scripts/run_security_scan.py
```

Outputs:
- Latest report: reports/gitleaks-latest.json
- History: reports/gitleaks-history.json

CI integration examples:
- Use your CI runner to install GitLeaks via the OS package manager
- Then run: python scripts/run_security_scan.py

Build failure conditions:
- Critical secrets found
- Scanner errors occur

## Database Utilities

Quick connectivity check from Python REPL:

```
from database.models import test_connection, create_tables
print("DB OK:", test_connection())
create_tables()
```

Seeding:

```
from database.seed_data import seed_database
seed_database()
```

## Git Workflow for Team

1) Create a feature branch
```
git checkout -b feat/<short-description>
```
2) Ensure code quality locally
```
pip install -r requirements.txt
pytest -q
python scripts/run_security_scan.py
```
3) Commit and push
```
git add -A
git commit -m "feat: <summary>"
git push origin feat/<short-description>
```
4) Open a pull request for review

## Troubleshooting

- DATABASE_URL is None
  - Ensure .env exists at project root and contains DATABASE_URL
  - Confirm the .env format is correct; run `python -c "import os; print(os.getcwd())"` to verify your CWD when running commands
- Authentication fails with 401
  - Verify the Authorization header is set: `Authorization: Bearer <token>`
  - Regenerate token via /auth/login
- MySQL connection errors
  - Validate host, port, user, password in DATABASE_URL
  - Confirm MySQL server is running and user has privileges on the target database

## License

This project is intended for educational and team demonstration purposes.
