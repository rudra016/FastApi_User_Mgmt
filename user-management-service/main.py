from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import userOutput
@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Starting")
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/protected")
def read_protected(user : userOutput = Depends(get_current_user)):
    return {"data": user}