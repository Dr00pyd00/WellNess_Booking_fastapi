from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # en dev pour que pydantic sache ou aller chercher le fichier:
    model_config=ConfigDict(env_file=".env")

    # postgres:
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_port: int 
    postgres_host: str


    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}"
            f":{self.postgres_password}"
            f"@{self.postgres_host}"
            f":{self.postgres_port}"
            f"/{self.postgres_db}"
        )




# creer une instance pour l'use:
app_settings = Settings()
