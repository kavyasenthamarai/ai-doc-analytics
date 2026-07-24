import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentStatus
from app.schemas.document import DocumentResponse
from app.services.parsing import parse_document_task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_CONTENT_TYPES = {"application/pdf"}

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    file_size = len(contents)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 10MB limit")

    if file_size == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    user = db.query(User).filter(User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except OSError:
        logger.error(f"Failed to save file for user {current_user_email}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to save file")

    try:
        new_document = Document(
            user_id=user.id,
            original_filename=file.filename,
            stored_filename=safe_filename,
            file_size_bytes=file_size,
            status=DocumentStatus.UPLOADED,
        )
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
    except Exception:
        os.remove(file_path)
        db.rollback()
        logger.error(f"Failed to save document record for user {current_user_email}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to record document")

    logger.info(f"Document uploaded: {file.filename} by {current_user_email}")
    return new_document


@router.post("/{document_id}/parse")
def trigger_parse(
    document_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user_email: str = Depends(get_current_user),
):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    user = db.query(User).filter(User.email == current_user_email).first()
    if document.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this document")

    file_path = os.path.join(UPLOAD_DIR, document.stored_filename)
    background_tasks.add_task(parse_document_task, document.id, file_path)

    return {"message": "Parsing started", "document_id": document.id}