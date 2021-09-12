import os
from dotenv import load_dotenv
import uvicorn
from auth_routes import auth_router
from order_routes import order_router
from tortoise.contrib.fastapi import register_tortoise

from fastapi import FastAPI

app = FastAPI(title='Pizza Delivery Application')

load_dotenv()

app.include_router(auth_router)
app.include_router(order_router)


DB_TYPE = os.getenv('DB_TYPE')
DB_USER = os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DB_NAME = os.getenv('DB_NAME')

register_tortoise(
    app,
    db_url=f'{DB_TYPE}://{DB_USER}:{PASSWORD}@{HOST}/{DB_NAME}',
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
