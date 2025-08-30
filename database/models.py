from sqlalchemy import Column, Integer, String, DateTime, Text, create_engine, text as sa_text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Get DB URL from .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Baroda%40123@localhost:3306/medical_records"
)

# Setup engine and session
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(String(10), nullable=False)
    contact = Column(String(50), nullable=False)
    diagnosis = Column(Text, nullable=True)
    prescriptions = Column(Text, nullable=True)
    doctor = Column(String(100), nullable=False)
    visit_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def test_connection() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(sa_text("SELECT 1"))
        return True
    except Exception:
        return False


def create_tables():
    Base.metadata.create_all(bind=engine)


def init_db():
    create_tables()
