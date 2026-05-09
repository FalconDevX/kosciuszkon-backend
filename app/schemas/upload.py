from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    filename: str
    saved_path: str
    size_bytes: int
