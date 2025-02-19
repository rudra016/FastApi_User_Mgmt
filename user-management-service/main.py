from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter

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