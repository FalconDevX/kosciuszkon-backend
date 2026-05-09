from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.upload import FileUploadResponse
from app.services.upload_service import FileTooLargeError, save_upload

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        saved_path, size = await save_upload(file)
    except FileTooLargeError:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum size of {settings.MAX_UPLOAD_BYTES} bytes",
        )

    return FileUploadResponse(
        filename=file.filename or saved_path,
        saved_path=saved_path,
        size_bytes=size,
    )
