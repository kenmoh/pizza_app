from models import Order, OrderIn_Pydantic, Order_Pydantic, User
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi_jwt_auth.auth_jwt import AuthJWT


order_router = APIRouter(
    prefix='/order',
    tags=['orders']
)


@order_router.get('/')
async def order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {'message': 'hello order route'}


@order_router.post('/place_order', response_model=Order_Pydantic, status_code=status.HTTP_201_CREATED)
async def place_order(order: OrderIn_Pydantic, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORISED, detail="Invalid Token")

    current_user = Authorize.get_jwt_subject()

    # user = await User.get(username=current_user).first()

    new_order = await Order.create(
        pizza_size=order.pizza_size,
        qty=order.qty,
        order_status=order.order_status,
        order_by=await User.get(username=current_user).first()
    )
    # new_order.order_by = user

    await new_order.save()
    return new_order
