from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from models import User,  User_Pydantic, UserIn_Pydantic

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@auth_router.get('/users', response_model=List[User_Pydantic], status_code=status.HTTP_200_OK)
async def get_all_users():
    users = await User_Pydantic.from_queryset(User.all().order_by('-created_at'))
    return users


@auth_router.post('/register', response_model=User_Pydantic, status_code=status.HTTP_201_CREATED)
async def register(users: UserIn_Pydantic):
    db_username = await User.get_or_none(username=users.username)
    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this username already exist")

    db_email = await User.get_or_none(email=users.email)
    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User with this email already exist")

    new_user = await User.create(
        username=users.username,
        email=users.email,
        password=generate_password_hash(users.password),
        is_active=users.is_active,
        is_staff=users.is_staff,
    )

    await new_user.save()
    return new_user


@auth_router.get('/users/{user_id}', response_model=User_Pydantic, status_code=status.HTTP_200_OK)
async def get_single_user(user_id: str,):
    user = await User_Pydantic.from_queryset_single(User.get(id=user_id))
    return user


@auth_router.put('/users/{user_id}', response_model=User_Pydantic, status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: UserIn_Pydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@auth_router.delete('/users/{user_id}')
async def delete_user(user_id: str):
    user = await User.filter(id=user_id).delete()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found")
    return {"message": f'User with ID {user_id} deleted successfully!'}


@auth_router.delete('/users')  # For Testing purposes only
async def delete_users():
    await User.all().delete()
    return {"message": f"Users deleted successfully!"}
