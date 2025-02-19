from .base import BaseRepository
from app.db.models.user import User
from app.db.schema.user import UserInCreate, UserInLogin


class UserRepository(BaseRepository):
    def create_user(self, user_data: UserInCreate):
        newUser = User(**user_data.model_dump(exclude_none=True))
        self.session.add(newUser)
        self.session.commit()
        self.session.refresh(newUser)
        return newUser
    
    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter(User.email == email).first()
        return bool(user)
    
    def get_user_by_email(self, email: str) -> User:
        user = self.session.query(User).filter(User.email == email).first()
        return user
    
    def get_user_by_id(self, user_id : int):
        user = self.session.query(User).filter(id == user_id).first()
        return user