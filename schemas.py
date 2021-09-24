from enum import Enum
import os
from typing import Optional
from pydantic.networks import EmailStr
from pydantic import BaseModel  # EmailStr

from dotenv import load_dotenv
from pydantic.types import conlist

load_dotenv()


class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv('JWT_SECRET_KEY')


# USER SCHEMA
class Register(BaseModel):
    username: str
    email: EmailStr
    password: str


class EditUser(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    is_staff: Optional[bool]
    is_superuser: Optional[bool]


class LoginModel(BaseModel):
    username: str
    password: str


# ORDER SCHEMA
class OrderStatusEnum(str, Enum):
    PENDING: str = 'PENDING'
    IN_TRANSIT: str = 'IN-TRANSIT'
    DELIVERED: str = 'DELIVERED'


class OrderStatus(BaseModel):
    order_status: OrderStatusEnum


class PizzaSize(str, Enum):
    SMALL: str = 'SMALL'
    MEDIUM: str = 'MEDIUM'
    LARGE: str = 'LARGE'
    XTRA_LARGE: str = 'XTRA-LARGE'


class OrderModel(BaseModel):
    qty: int
    pizza_size: PizzaSize
