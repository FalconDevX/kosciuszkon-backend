import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings


class FileTooLargeError(Exception):
    pass


async def save_upload(file: UploadFile) -> tuple[str, int]:
    root = Path(settings.UPLOAD_DIR)
    root.mkdir(parents=True, exist_ok=True)

    original = file.filename or "upload"
    safe_name = Path(original).name
    if not safe_name or safe_name in (".", ".."):
        safe_name = "upload"

    dest_name = f"{uuid.uuid4().hex}_{safe_name}"
    dest = root / dest_name

    size = 0
    chunk = 1024 * 1024
    try:
        with dest.open("wb") as out:
            while True:
                block = await file.read(chunk)
                if not block:
                    break
                size += len(block)
                if size > settings.MAX_UPLOAD_BYTES:
                    raise FileTooLargeError()
                out.write(block)
    except FileTooLargeError:
        dest.unlink(missing_ok=True)
        raise
    except Exception:
        dest.unlink(missing_ok=True)
        raise

    return str(dest.resolve()), size
