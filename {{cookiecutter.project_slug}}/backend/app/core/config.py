import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, RedisDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    PROJECT_DESCRIPTION = "{{cookiecutter.project_description}}"
    SERVER_HOST: str = os.getenv("DOMAIN")
    API_V1_STR: str = "/api/v1"
    API_V1_VERSION = "1.0.0"
    BASE_DIR: str = os.path.dirname(os.path.realpath(__file__))

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    HASH_ALGORITHM: str = "HS256"

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = os.getenv("DATABASE_URL", None)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # Celery
    CELERY_BROKER_URL: RedisDsn = os.getenv("CELERY_BROKER_URL")

    # Mailing
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = os.getenv("SMTP_PORT")
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST")
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = os.path.join(BASE_DIR, "templates/")
    EMAILS_ENABLED: bool = False

    # Authentication
    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")
    ACCESS_TOKEN_EXPIRATION: int = 60 * 24  # in minutes
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
