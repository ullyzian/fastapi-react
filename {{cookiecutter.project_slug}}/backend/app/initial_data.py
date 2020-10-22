#!/usr/bin/env python3
import os

from app.crud.user import create_user
from app.core.database import SessionLocal
from app.schemas.user import UserCreate


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            email=os.getenv("SUPERUSER_EMAIL"),
            password=os.getenv("SUPERUSER_PASSWORD"),
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser {{cookiecutter.superuser_email}}")
    init()
    print("Superuser created")
