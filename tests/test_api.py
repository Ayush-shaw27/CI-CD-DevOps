import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, get_db
from main import app
import os

# Test database setup - MySQL test database
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/medical_records_test"
)

engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Setup test database"""
    try:
        Base.metadata.create_all(bind=engine)
        yield
        Base.metadata.drop_all(bind=engine)
    except Exception as e:
        print(f"Error setting up MySQL test database: {e}")
        print("Please ensure MySQL server is running and test database 'medical_records_test' exists")
        pytest.skip("MySQL test database not available")

def test_register_user(setup_database):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "username": "testdoctor",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "doctor"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testdoctor"
    assert data["role"] == "doctor"

def test_login_user(setup_database):
    """Test user login"""
    # First register a user
    client.post(
        "/auth/register",
        json={
            "username": "logintest",
            "email": "login@example.com",
            "password": "testpass123",
            "role": "doctor"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        json={
            "username": "logintest",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_patient_unauthorized():
    """Test creating patient without authentication"""
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "date_of_birth": "1990-01-01",
            "contact": "555-0123",
            "doctor": "Dr. Test"
        }
    )
    assert response.status_code == 401

def test_create_patient_authorized(setup_database):
    """Test creating patient with authentication"""
    # Register and login
    client.post(
        "/auth/register",
        json={
            "username": "patienttest",
            "email": "patient@example.com",
            "password": "testpass123",
            "role": "doctor"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "username": "patienttest",
            "password": "testpass123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Create patient
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "date_of_birth": "1990-01-01",
            "contact": "555-0123",
            "doctor": "Dr. Test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Patient"
    assert data["doctor"] == "Dr. Test"
