from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PatientBase(BaseModel):
    name: str
    date_of_birth: str
    contact: str
    diagnosis: Optional[str] = None
    prescriptions: Optional[str] = None
    doctor: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[str] = None
    contact: Optional[str] = None
    diagnosis: Optional[str] = None
    prescriptions: Optional[str] = None
    doctor: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    visit_date: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
