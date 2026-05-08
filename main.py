from dotenv import load_dotenv
from fastapi import FastAPI

from routes import ai_router, auth_router, users_router

load_dotenv()

app = FastAPI(title="Kościuszkon API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(ai_router)


@app.get("/")
async def root():
    return {"message": "FastAPI works"}
