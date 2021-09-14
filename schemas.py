import os
from typing import Optional
from pydantic.networks import EmailStr
from pydantic import BaseModel  # EmailStr

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')


class Register(BaseModel):
    username: str
    email: str
    password: str


class EditUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_staff: Optional[bool]


class LoginModel(BaseModel):
    username: str
    password: str
