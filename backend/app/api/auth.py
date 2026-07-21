from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

fake_users_db = {}

@router.post("/register")
def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    fake_users_db[user.email] = {"email": user.email, "hashed_password": hashed}

    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    db_user = fake_users_db.get(user.email)

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}