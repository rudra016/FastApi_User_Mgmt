import jwt
from decouple import config
import time

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')
ACCESS_TOKEN_EXPIRE = 5600  # 1.5 hours

class AuthHandler(object):

    @staticmethod
    def sign_jwt(user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + ACCESS_TOKEN_EXPIRE
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    
    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["expires"] >= time.time() else {"error": "Token has expired"}
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}