from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.core.database import get_db
from app.service.userService import UserService
from app.db.schema.user import userOutput
import redis.asyncio as redis
import json


AUTH_PREFIX = 'Bearer '

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

async def get_current_user(session: Session = Depends(get_db), authorization : Annotated[Union[str, None], Header()] = None)-> userOutput:
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    if not authorization:
        raise auth_exception
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception
    payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])
    user_id = payload.get("user_id")
    cached_user = await redis_client.get(f"user:{user_id}")
    if cached_user:
        print("Fetching user from Redis cache")
        return userOutput(**json.loads(cached_user))

    try:
        user = UserService(session=session).get_user_by_id(payload["user_id"])
        return userOutput(
        id = user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
        )
    except Exception as e:
        raise auth_exception
    