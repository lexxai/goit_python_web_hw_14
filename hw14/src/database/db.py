import logging
from fastapi import HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import redis.asyncio as redis

from src.conf.config import settings

logger = logging.getLogger(f"{settings.app_name}.{__name__}")

URI = settings.sqlalchemy_database_url
SQLALCHEMY_DATABASE_URL = URI

assert SQLALCHEMY_DATABASE_URL is not None, "SQLALCHEMY_DATABASE_URL UNDEFINED"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=(settings.app_mode == "dev"))


DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        print("SQLAlchemyError:", err)
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()


def create_redis():
    return redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=False)


def get_redis() -> redis.Redis:
    # Here, we re-use our connection pool
    # not creating a new one
    logger.debug("get_redis connection_pool")
    connection = redis.Redis(connection_pool=redis_pool)
    return connection


redis_pool: redis.ConnectionPool = create_redis()
