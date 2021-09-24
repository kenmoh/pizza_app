from typing import List

from fastapi.encoders import jsonable_encoder
from schemas import OrderModel, OrderStatus
from models import Order, OrderIn_Pydantic, Order_Pydantic, User, User_Pydantic
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT
from tortoise.query_utils import Q


order_router = APIRouter(
    prefix='/order',
    tags=['orders']
)


def authorize_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    current_user = Authorize.get_jwt_subject()
    return current_user


@order_router.get('/')
async def order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {'message': 'hello order route'}


@order_router.post('/place_order', status_code=status.HTTP_201_CREATED)
async def place_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED, detail="Invalid Token")

    current_user = Authorize.get_jwt_subject()

    user = await User_Pydantic.from_queryset_single(User.get(username=current_user))

    new_order = await Order(
        pizza_size=order.pizza_size,
        qty=order.qty,
    )
    new_order.user = user

    await new_order.save()
    response = {
        "user": user.email,
        "order": new_order
    }
    return jsonable_encoder(response)


@order_router.get('/orders', response_model=List[Order_Pydantic], status_code=status.HTTP_200_OK)
async def list_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()

    user = await User.get(username=current_user).first()
    if user.is_staff:
        orders = await Order_Pydantic.from_queryset(Order.all().order_by('-created_at'))
        return orders
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not authorized to carry out this operation!")


@order_router.get('/{order_id}', response_model=Order_Pydantic, status_code=status.HTTP_200_OK)
async def get_by_id(order_id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED, detail='Invalid Token')
    order = await Order_Pydantic.from_queryset_single(Order.get(id=order_id))

    try:
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="No order with that id exists!")


@order_router.get('/user_orders/{login_user}')
async def get_order_by_user(login_user: str, Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED, detail='Invalid Token')
    current_user = Authorize.get_jwt_subject()
    user = await User_Pydantic.from_queryset_single(User.get(username=current_user))
    if login_user == user.username:
        user_orders = await Order_Pydantic.from_queryset(Order.all().filter(Q(user=login_user) and Q(user=user.username)))
        return user_orders
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")


@order_router.put('/update/{order_id}', response_model=Order_Pydantic, status_code=status.HTTP_200_OK)
async def update_by_order_id(order_id: str, order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED, detail='Invalid Token')
    db_order = await Order.get(id=order_id)
    db_order.qty = order.qty
    db_order.pizza_size = order.pizza_size
    await db_order.save()
    return db_order


@order_router.put('/update_order_status/{order_id}', response_model=Order_Pydantic, status_code=status.HTTP_200_OK)
async def update_order_status(order_id, order: OrderStatus, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')

    current_user = Authorize.get_jwt_subject()

    user = await User.get(username=current_user).first()
    if user.is_staff:
        db_order_status = await Order.get(id=order_id)
        db_order_status.order_status = order.order_status
        await db_order_status.save()
        return db_order_status
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You are not authorized to carry out this operation!")
