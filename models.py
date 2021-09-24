from pydantic.types import conlist
from schemas import OrderStatus, OrderStatusEnum, PizzaSize
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    is_staff = fields.BooleanField(default=False, null=True)
    is_superuser = fields.BooleanField(default=False, null=True)
    is_active = fields.BooleanField(default=False, null=True)
    order: fields.ReverseRelation['Order']
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = 'users'


class Order(models.Model):

    id = fields.UUIDField(pk=True)
    qty = fields.IntField(null=False)
    order_status: OrderStatusEnum = fields.CharField(
        default='PENDING', max_length=255)
    pizza_size: PizzaSize = fields.CharField(default='SMALL', max_length=255)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        'models.User', on_delete=fields.CASCADE, related_name='orders', to_field='username')
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
