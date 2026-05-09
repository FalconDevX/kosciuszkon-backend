from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserRead, UserUpdate
from app.services.user_service import (
    delete_user,
    get_user,
    login_user,
    register_user,
    update_user,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        created_user = await register_user(db, user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists")

    return created_user


@router.post("/login", response_model=UserRead)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    logged_user = await login_user(db, user)

    if not logged_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return logged_user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def edit_user(user_id: str, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_user = await update_user(db, user_id, user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists")

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@router.delete("/{user_id}")
async def remove_user(user_id: str, db: AsyncSession = Depends(get_db)):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

