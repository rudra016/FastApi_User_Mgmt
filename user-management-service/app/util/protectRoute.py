from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.core.database import get_db
from app.service.userService import UserService
from app.db.schema.user import userOutput

AUTH_PREFIX = 'Bearer '


def get_current_user(session: Session = Depends(get_db), authorization : Annotated[Union[str, None], Header()] = None)-> userOutput:
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    if not authorization:
        raise auth_exception
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception
    payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])

    if payload and payload["user_id"]:
        user = UserService(session=session).get_user_by_id(user_id=payload["user_id"])
        if user:
            return userOutput(
                id = user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        raise auth_exception
    raise auth_exception