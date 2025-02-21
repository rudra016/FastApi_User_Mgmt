from pydantic import EmailStr, BaseModel
from typing import Union

class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class userOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserInUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str