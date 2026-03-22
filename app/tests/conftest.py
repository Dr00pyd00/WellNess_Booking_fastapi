import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.database import Base
from app.dependencies.database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import app_settings


POSTGRES_URL_DB = app_settings.test_db_url

test_engine = create_async_engine(
    url=POSTGRES_URL_DB,
)

TestLocalSession = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


# On creer des fixtures pour mimer les element et fonctions:
@pytest.fixture(scope="function")
async def db_session():

    # a l'appel de la db on creer les tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    async with TestLocalSession() as db:
        yield db
        # a la fin du gen, on delete toutes les tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


# on creer un client ( un genre de postman maison):
@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):


    # la fonction qui override:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] =  override_get_db


    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac


    app.dependency_overrides.clear()
    