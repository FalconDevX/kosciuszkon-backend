import os
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

try:
    from supabase import Client, create_client
except ImportError:  # pragma: no cover
    Client = object  # type: ignore[misc, assignment]
    create_client = None  # type: ignore[misc, assignment]

_supabase: Optional["Client"] = None


def get_supabase() -> Optional["Client"]:
    global _supabase
    if _supabase is not None:
        return _supabase
    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if not url or not key or create_client is None:
        return None
    _supabase = create_client(url, key)
    return _supabase


@lru_cache
def is_supabase_configured() -> bool:
    return bool(os.getenv("SUPABASE_URL", "").strip()) and bool(
        os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    )
