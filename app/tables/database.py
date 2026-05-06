import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


sessions_map = {}
allowed_users = ["DJANGO", "QGIS", "BOT", "RIGHTFUL"]


def check_user(user: str) -> bool:
    if user in allowed_users:
        return True
    return False


async def get_db_asession(user: str) -> AsyncSession | None:
    if check_user(user.upper()):
        return sessions_map[user.upper()]()
    return None


def init_asessions():
    db_current_host = f"{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}"


    for user in allowed_users:
        db_current_user = os.getenv(f"POSTGRES_{user.upper()}_USER")
        db_current_password = os.getenv(f"POSTGRES_{user.upper()}_PASSWORD")
        db_current_url = f"postgresql+asyncpg://{db_current_user}:{db_current_password}@{db_current_host}"


        engine = create_async_engine(
            url=db_current_url,
            pool_size=20,
            max_overflow=10,
            pool_recycle=3600,
        )


        sessions_map[user] = async_sessionmaker(
            engine, 
            class_=AsyncSession, 
            expire_on_commit=False
        )


class Base(DeclarativeBase):
    pass
