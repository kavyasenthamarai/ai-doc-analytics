from fastapi import FastAPI
from app.api import auth
from app.core.database import Base, engine
from app.models import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "AI Document Analytics Platform - API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}