from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def test():
    return {"message": "Users route works"}

