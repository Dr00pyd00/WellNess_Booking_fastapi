from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


from app.core.config import app_settings


# TOUT en async pour taches comlplexes.

engine = create_async_engine(url=app_settings.db_url)

LocalSession = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# avec class car non deprecié:
class Base(DeclarativeBase):
    pass

