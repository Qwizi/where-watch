import os
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from models import Site


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI):
    register_tortoise(
        app,
        db_url=os.environ.get(
            "DATABASE_URL", "postgres://where_watch:where_watch@db:5432/where_watch"),
        modules={'models': ['models', 'aerich.models']},
        generate_schemas=True,
        add_exception_handlers=True
    )
    Tortoise.init_models(['models'], 'models')
