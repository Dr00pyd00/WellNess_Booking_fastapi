import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.core.database import Base
from app.dependencies.database import get_db
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import app_settings

# ===================================== #
# ======== GLOBAL    ================== #
# ===================================== #

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
    # test_engine.begin() : ouvre une co a la DB,
    # comme c'est async on met await
    async with test_engine.begin() as conn:
        # on creer les table avec le traducteur run_sync
        await conn.run_sync(Base.metadata.create_all)

    # ouvre une session de travail avec la DB,
    async with TestLocalSession() as db:
        # yield met la fixture en pause , donne db puis quand fini: on continue
        yield db

    # meme bloc que le premier:
    # donne l'ordre de supprimer
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # ferme toutes les lignes
    # chaque commandes precedentes a ouvrest une canals differents 
    # on les fermes tous:
    await test_engine.dispose()

        


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
    



# ===================================== #
# ======== USERS PRESETS   ============ #
# ===================================== #

good_user_data = {
    "username":"usernametest",
    "password":"testpassword123",
    "email":"test@test.com",
    "phone_number":"123456789",
    "birth":"2000-02-02",
}

# Creer 1 user automatiquement:
@pytest.fixture
async def create_user_response(client: AsyncClient):
    response = await client.post(url="/users/", json=good_user_data)

    return response
