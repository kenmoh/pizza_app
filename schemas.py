import os
from pydantic.networks import EmailStr
from pydantic import BaseModel  # EmailStr

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')


class LoginModel(BaseModel):
    username: str
    password: str
