from fastapi import APIRouter, Depends, Request
from app.db.schema.user import UserInCreate, UserInLogin, UserWithToken, userOutput
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.userService import UserService
authRouter  = APIRouter()

@authRouter.post("/login", status_code=200, response_model=UserWithToken)
async def login(request: Request, loginDetails: UserInLogin, session: Session = Depends(get_db)):
    redis_client = request.app.state.redis
    return await UserService(session=session, redis_client=redis_client).login(login_details=loginDetails)


@authRouter.post("/signup", status_code=201, response_model=userOutput)
async def signup(request: Request, signupDetails: UserInCreate, session: Session = Depends(get_db)):
    redis_client = request.app.state.redis
    return await UserService(session=session, redis_client=redis_client).signup(user_details=signupDetails)
   