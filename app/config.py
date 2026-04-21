import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_INTERNAL_HOST: str
    DB_INTERNAL_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    SERVER_HOST: str
    SERVER_PORT: int
    FRONT_PORT: int

    model_config = SettingsConfigDict(
        # env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )
    # except:
    # print()
    # model_config = SettingsConfigDict(env_file=os.path.join('..', ".env"))

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_INTERNAL_HOST}:{self.DB_INTERNAL_PORT}/{self.DB_NAME}")

    def get_auth_data(self):
        return {"secret_key": self.SECRET_KEY, "algorithm": self.ALGORITHM}

    def get_data_for_db_external(self):
        return {"user": self.DB_USER, "password": self.DB_PASSWORD, "host": self.DB_HOST, "port": self.DB_PORT, "database": self.DB_NAME}

    def get_admin_data(self):
        return {"name": self.DB_USER, "email": self.DB_USER + '@mail.ru', "password": self.DB_PASSWORD}

settings = Settings()