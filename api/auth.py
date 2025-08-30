from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database.models import User, get_db
from api.schemas import UserLogin, UserCreate, UserResponse, Token
from auth.security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token"""
    # Input sanitization
    username = user_credentials.username.strip().lower()
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (for demo purposes)"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username.strip().lower()) |
        (User.email == user_data.email.lower())
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Validate role
    if user_data.role not in ["doctor", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be either 'doctor' or 'staff'"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username.strip().lower(),
        email=user_data.email.lower(),
        hashed_password=hashed_password,
        role=user_data.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse.model_validate(db_user)
