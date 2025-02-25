from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import userOutput
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
import os
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

origins = ["*"]

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)


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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)  # Send the error to Sentry
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."},
    )


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/protected", tags=["auth"])
def read_protected(user : userOutput = Depends(get_current_user)):
    return {"data": user}