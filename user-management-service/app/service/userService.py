from app.db.repository.userRepo import UserRepository
from app.db.schema.user import userOutput, UserInCreate, UserInLogin, UserWithToken
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException
import redis.asyncio as redis
from fastapi_cache.decorator import cache
import json
class UserService:
    def __init__(self, session: Session, redis_client: redis.Redis) -> None:
        self.__userRepository = UserRepository(session=session)
        self.redis = redis_client

    async def signup(self, user_details: UserInCreate) -> userOutput:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="User already exists")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        user = self.__userRepository.create_user(user_data=user_details)
        
        # Convert user object to dictionary and then to JSON before storing in Redis
        user_dict = userOutput.model_validate(user).model_dump() 
        await self.redis.set(f"user:{user.id}", json.dumps(user_dict), ex=5600)  
        
        return user
    
    async def login(self, login_details: UserInLogin) -> UserWithToken:
        if not self.__userRepository.user_exist_by_email(email=login_details.email):
            raise HTTPException(status_code=400, detail="Please create an account")
        
        user = self.__userRepository.get_user_by_email(email=login_details.email)
        
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                try:
                    # Try storing the token in Redis
                    await self.redis.set(f"token:{user.id}", token, ex=5600)
                except Exception as e:
                    print(f"Redis connection failed: {e}") 
                return UserWithToken(token=token)
            
            raise HTTPException(status_code=500, detail="Unable to process request")

        raise HTTPException(status_code=400, detail="Invalid credentials")

    
    @cache(expire=5600)
    async def get_user_by_id(self, user_id: int):
        cached_user = await self.redis.get(f"user:{user_id}")
        if cached_user:
            print("Cached User")
            return userOutput.model_validate_json(cached_user)
        print(user_id)
        user = self.__userRepository.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    
    async def logout(self, user_id: int) -> dict:
        # Remove user authentication token from cache
        await self.redis.delete(f"token:{user_id}")
        return {"message": "Logged out successfully"}