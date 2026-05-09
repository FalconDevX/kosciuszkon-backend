from app.core.security import verify_password
from app.crud import create_user as create_user_crud
from app.crud import delete_user as delete_user_crud
from app.crud import get_user_by_id
from app.crud import get_user_by_email
from app.crud import update_user as update_user_crud


async def register_user(db, user_data):
    return await create_user_crud(db, user_data)


async def login_user(db, user_data):
    user = await get_user_by_email(db, user_data.email)

    if not user:
        return None

    if not verify_password(user_data.password, user.password_hash):
        return None

    return user


async def get_user(db, user_id: str):
    return await get_user_by_id(db, user_id)


async def update_user(db, user_id: str, user_data):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    return await update_user_crud(db, user, user_data)


async def delete_user(db, user_id: str):
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await delete_user_crud(db, user)
    return True

