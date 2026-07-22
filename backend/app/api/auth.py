import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.core.database import get_db
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    normalized_email = user.email.lower().strip()

    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        hashed = hash_password(user.password)
        new_user = User(email=normalized_email, hashed_password=hashed)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError:
        db.rollback()
        logger.error(f"Database error during registration for {normalized_email}", exc_info=True)
        raise HTTPException(status_code=500, detail="Registration failed, please try again")

    logger.info(f"New user registered: {normalized_email}")
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    normalized_email = user.email.lower().strip()
    db_user = db.query(User).filter(User.email == normalized_email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logger.warning(f"Failed login attempt for {normalized_email}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": db_user.email})
    logger.info(f"User logged in: {normalized_email}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_current_user(current_user: str = Depends(get_current_user)):
    return {"email": current_user}