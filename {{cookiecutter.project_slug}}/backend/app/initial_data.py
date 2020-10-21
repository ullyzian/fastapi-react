#!/usr/bin/env python3

from app.crud.user import create_user
from app.db.session import SessionLocal
from app.schemas.user import UserCreate


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email="{{cookiecutter.superuser_email}}",
            password="{{cookiecutter.superuser_password}}",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser {{cookiecutter.superuser_email}}")
    init()
    print("Superuser created")
