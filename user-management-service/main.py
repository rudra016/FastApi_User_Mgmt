from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import userOutput
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
origins = ["*"]


@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Starting")
    create_tables()
    
    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    
    # Initialize FastAPI Cache with Redis
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
    app.state.redis = redis_client
    yield
    
    # Close Redis connection
    await redis_client.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/protected")
def read_protected(user : userOutput = Depends(get_current_user)):
    return {"data": user}