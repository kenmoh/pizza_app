import os
from aerich import Command
from dotenv import load_dotenv
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from tortoise import run_async
from fastapi_jwt_auth import AuthJWT

from fastapi import FastAPI

from schemas import Settings
from auth_routes import auth_router
from order_routes import order_router

app = FastAPI(title='Pizza Delivery Application')

load_dotenv()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(order_router)


DB_TYPE = os.getenv('DB_TYPE')
DB_USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DB_NAME = os.getenv('DB_NAME')


# TORTOISE_ORM = {
#     "connections": {"default": f'{DB_TYPE}://{DB_USER}:{PASSWORD}@{HOST}/{DB_NAME}'},
#     "apps": {
#         "models": {
#             "models": ["models", "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }

register_tortoise(
    app,
    db_url=f'{DB_TYPE}://{DB_USER}:{PASSWORD}@{HOST}/{DB_NAME}',
    modules={"models": ["models", "aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


if __name__ == "__main__":
    # run_async(config())
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
