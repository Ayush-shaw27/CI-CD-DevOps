# Medical Records Web Portal - DevSecOps Backend

A secure medical records management system with integrated DevSecOps security scanning for CI/CD pipelines.

## 🏗️ Project Structure

\`\`\`
medical-records-devsecops/
├── api/                    # API endpoints and schemas
│   ├── auth.py            # Authentication endpoints
│   ├── patients.py        # Patient CRUD operations
│   └── schemas.py         # Pydantic models
├── auth/                  # Authentication and security
│   ├── dependencies.py    # Auth dependencies
│   └── security.py        # JWT and password handling
├── database/              # Database models and setup
│   ├── models.py          # SQLAlchemy models
│   └── seed_data.py       # Database seeding
├── scanner/               # DevSecOps security scanning
│   ├── __init__.py
│   └── gitleaks_scanner.py # GitLeaks integration
├── scripts/               # Utility scripts
│   └── run_security_scan.py # CI/CD security scan script
├── tests/                 # Unit tests
│   ├── test_api.py        # API endpoint tests
│   └── test_scanner.py    # Scanner module tests
├── reports/               # Generated security reports
├── main.py                # FastAPI application
└── requirements.txt       # Python dependencies
\`\`\`

## 🚀 Quick Start

### 1. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Setup MySQL Database

**Install MySQL Server:**
\`\`\`bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# macOS
brew install mysql

# Windows
# Download from https://dev.mysql.com/downloads/mysql/
\`\`\`

**Create Database:**
\`\`\`sql
mysql -u root -p
CREATE DATABASE medical_records;
CREATE DATABASE medical_records_test; -- For testing
GRANT ALL PRIVILEGES ON medical_records.* TO 'root'@'localhost';
GRANT ALL PRIVILEGES ON medical_records_test.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
\`\`\`

### 3. Configure Database Connection

Set environment variable or update `database/models.py`:
\`\`\`bash
export DATABASE_URL="mysql+pymysql://root:password@localhost:3306/medical_records"
\`\`\`

### 4. Initialize Database

\`\`\`bash
python database/seed_data.py
\`\`\`

### 5. Run the Application

\`\`\`bash
python main.py
\`\`\`

The API will be available at `http://localhost:8000`

### 6. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔐 Authentication

### Default Users (for testing)

- **Doctor**: `dr_smith` / `doctor123`
- **Staff**: `nurse_jane` / `staff123`

### Login Process

1. POST `/auth/login` with credentials
2. Receive JWT token in response
3. Include token in Authorization header: `Bearer <token>`

## 📋 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Patients (Requires Authentication)
- `GET /patients/` - List all patients
- `GET /patients/{id}` - Get specific patient
- `POST /patients/` - Create new patient
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient

### System
- `GET /` - API information
- `GET /health` - Health check

## 🔒 DevSecOps Integration

### Security Scanning

The project includes GitLeaks integration for secret detection in CI/CD pipelines.

#### Manual Scan

\`\`\`bash
python scripts/run_security_scan.py
\`\`\`

#### CI/CD Integration

Add to your pipeline configuration:

**GitHub Actions:**
\`\`\`yaml
- name: Security Scan
  run: python scripts/run_security_scan.py
\`\`\`

**Jenkins:**
\`\`\`groovy
stage('Security Scan') {
    steps {
        sh 'python scripts/run_security_scan.py'
    }
}
\`\`\`

**GitLab CI:**
\`\`\`yaml
security_scan:
  script:
    - python scripts/run_security_scan.py
\`\`\`

### Scan Reports

- Latest scan: `reports/gitleaks-latest.json`
- Scan history: `reports/gitleaks-history.json`

### Build Failure Conditions

The build will fail if:
- Critical secrets are detected (AWS keys, API tokens, passwords)
- Scanner encounters errors
- Exit code 1 is returned for CI/CD integration

## 🧪 Testing

### Prerequisites for Testing

Ensure MySQL test database exists:
\`\`\`sql
CREATE DATABASE medical_records_test;
\`\`\`

Set test database URL:
\`\`\`bash
export TEST_DATABASE_URL="mysql+pymysql://root:password@localhost:3306/medical_records_test"
\`\`\`

### Run Unit Tests

\`\`\`bash
pytest tests/
\`\`\`

### Run Specific Test Files

\`\`\`bash
pytest tests/test_api.py
pytest tests/test_scanner.py
\`\`\`

### Test Coverage

\`\`\`bash
pytest --cov=. tests/
\`\`\`

## 🛡️ Security Features

### Input Validation
- All user inputs are validated and sanitized
- SQL injection protection via SQLAlchemy ORM
- XSS prevention through proper data handling

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (doctor/staff)
- Secure password hashing with bcrypt

### DevSecOps Integration
- Automated secret scanning with GitLeaks
- CI/CD pipeline integration
- Security report generation
- Build failure on critical findings

## 🔧 Configuration

### Environment Variables

Create a `.env` file for production:

\`\`\`env
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/medical_records
TEST_DATABASE_URL=mysql+pymysql://username:password@localhost:3306/medical_records_test
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

### Database Configuration

The application now uses MySQL by default. Connection string format:
\`\`\`
mysql+pymysql://username:password@host:port/database_name
\`\`\`

**Production MySQL Setup:**
- Use strong passwords for database users
- Enable SSL connections for remote databases
- Configure proper user privileges (avoid using root in production)
- Set up regular database backups

## 📊 Example Patient Data

The system includes sample patient records:

1. **John Doe** - Hypertension, Type 2 Diabetes
2. **Jane Wilson** - Seasonal Allergies  
3. **Robert Johnson** - Lower Back Pain

## 🚨 Security Considerations

### Production Deployment

1. **Change default secret key** in `auth/security.py`
2. **Use environment variables** for sensitive configuration
3. **Enable HTTPS** for all communications
4. **Implement rate limiting** for API endpoints
5. **Use production MySQL setup** with proper user privileges
6. **Enable MySQL SSL connections** for remote databases
7. **Enable logging and monitoring**

### CI/CD Security

1. **Run security scans** on every commit
2. **Fail builds** on critical security findings
3. **Store scan reports** for audit trails
4. **Monitor for new vulnerabilities** regularly

## 📝 Development Notes

- Built with FastAPI for high performance and automatic API documentation
- Uses SQLAlchemy ORM with MySQL database for production-ready data storage
- Implements JWT authentication with role-based access
- Includes comprehensive error handling and input validation
- Follows REST API best practices
- Integrates with DevSecOps tools for security scanning
- MySQL provides ACID compliance and better concurrent access than SQLite

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run security scans: `python scripts/run_security_scan.py`
4. Run tests: `pytest tests/`
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes.
