from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr
from pydantic.schema import encode_default
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    is_staff = fields.BooleanField(blank=True, default=False)
    is_active = fields.BooleanField(blank=True, default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'users'


# class CreateUser(BaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     is_staff: bool
#     is_active: bool


class Order(models.Model):

    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('IN TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
    )

    PIZZA_SIZES = (
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large')
    )

    id = fields.UUIDField(pk=True)
    qty = fields.IntField(null=False)
    order_status = fields.CharField(
        choices=ORDER_STATUS, default='PENDING', max_length=255)
    pizza_size = fields.CharField(
        choices=PIZZA_SIZES, default='SMALL', max_length=255)
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_by = fields.ForeignKeyField(
        'models.User', on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'orders'


# Pydantic Models
User_Pydantic = pydantic_model_creator(
    User, name="User", exclude=('created_at', 'modified_at', 'password'))
UserIn_Pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True)

Order_Pydantic = pydantic_model_creator(
    Order, name="Order", exclude=('created_at', 'modified_at'))
OrderIn_Pydantic = pydantic_model_creator(
    Order, name="OrderIn", exclude_readonly=True)
