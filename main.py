from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes.users import router as users_router

load_dotenv()

app = FastAPI(title="Kościuszkon API")

app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "FastAPI works"}
