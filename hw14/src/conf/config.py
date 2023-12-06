from os import environ
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ConfigDict, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_PATH_PROJECT = Path(__file__).resolve().parent.parent.parent
BASE_PATH = BASE_PATH_PROJECT.parent
load_dotenv(BASE_PATH.joinpath(".env"))
APP_ENV = environ.get("APP_ENV")
# print(APP_ENV)

# SQLALCHEMY_DATABASE_URL=postgresql+psycopg2://${POSTGRES_USERNAME}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=BASE_PATH.joinpath(f".env-{APP_ENV}") if APP_ENV else BASE_PATH.joinpath(".env"),
        env_file_encoding="utf-8",
    )

    app_mode: str = "prod"
    app_version: str = "hw"
    app_name: str = "contacts"
    app_host: str = "0.0.0.0"
    app_port: int = 9000
    sqlalchemy_database_url: str | None = None
    token_secret_key: str = "some_SuPeR_key"
    token_algorithm: str = "HS256"
    mail_username: str = "user@example.com"
    mail_password: str = ""
    mail_from: str = "user@example.com"
    mail_port: int = 465
    mail_server: str = ""
    mail_from_name: str = ""
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    cloudinary_name: str = "some_name"
    cloudinary_api_key: str = "0000000000000"
    cloudinary_api_secret: str = "some_secret"
    reate_limiter_times: int = 2
    reate_limiter_seconds: int = 5
    SPHINX_DIRECTORY: str = str(BASE_PATH_PROJECT.joinpath("docs", "_build", "html"))
    STATIC_DIRECTORY: str = str(BASE_PATH_PROJECT.joinpath("static"))

    # class Config:
    #     extra = "ignore"
    #     # TESTED FIRST USED ENV variables, even if file defined.
    #     env_file = BASE_PATH.joinpath(f".env-{APP_ENV}") if APP_ENV else BASE_PATH.joinpath(".env")
    #     env_file_encoding = "utf-8"


settings = Settings()

if __name__ == "__main__":
    print(settings.Config.env_file)
    print(settings)
