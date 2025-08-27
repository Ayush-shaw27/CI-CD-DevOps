from sqlalchemy.orm import Session
from database.models import Patient, User, SessionLocal, create_tables
from auth.security import get_password_hash
from datetime import datetime, timedelta

def seed_database():
    """Seed database with example data"""
    try:
        create_tables()
        db = SessionLocal()
    except Exception as e:
        print(f"Error connecting to MySQL database: {e}")
        print("Please ensure MySQL server is running and database 'medical_records' exists")
        return
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already seeded")
            return
        
        # Create example users
        users = [
            User(
                username="dr_smith",
                email="dr.smith@hospital.com",
                hashed_password=get_password_hash("doctor123"),
                role="doctor"
            ),
            User(
                username="nurse_jane",
                email="jane@hospital.com",
                hashed_password=get_password_hash("staff123"),
                role="staff"
            )
        ]
        
        for user in users:
            db.add(user)
        
        # Create example patients
        patients = [
            Patient(
                name="John Doe",
                date_of_birth="1985-03-15",
                contact="555-0101",
                diagnosis="Hypertension, Type 2 Diabetes",
                prescriptions="Metformin 500mg twice daily, Lisinopril 10mg once daily",
                doctor="Dr. Smith",
                visit_date=datetime.now() - timedelta(days=7)
            ),
            Patient(
                name="Jane Wilson",
                date_of_birth="1992-07-22",
                contact="555-0102",
                diagnosis="Seasonal Allergies",
                prescriptions="Claritin 10mg once daily as needed",
                doctor="Dr. Smith",
                visit_date=datetime.now() - timedelta(days=3)
            ),
            Patient(
                name="Robert Johnson",
                date_of_birth="1978-11-08",
                contact="555-0103",
                diagnosis="Lower Back Pain",
                prescriptions="Ibuprofen 400mg three times daily, Physical therapy",
                doctor="Dr. Smith",
                visit_date=datetime.now() - timedelta(days=1)
            )
        ]
        
        for patient in patients:
            db.add(patient)
        
        db.commit()
        print("MySQL database seeded successfully")
        
    except Exception as e:
        print(f"Error seeding MySQL database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
