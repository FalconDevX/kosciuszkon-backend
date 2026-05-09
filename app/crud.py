from sqlalchemy import select

from app.core.security import hash_password
from app.models import User


async def create_user(db, user_data):
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_email(db, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db, user_id: str):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def update_user(db, user, user_data):
    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        return user

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db, user):
    await db.delete(user)
    await db.commit()

