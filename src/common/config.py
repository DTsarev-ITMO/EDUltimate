import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_EXTERNAL_IP = os.environ.get("DB_EXTERNAL_IP")
DB_EXTERNAL_PORT = os.environ.get("DB_EXTERNAL_PORT")
DB_INTERNAL_IP = os.environ.get("DB_INTERNAL_IP")
DB_INTERNAL_PORT = os.environ.get("DB_INTERNAL_PORT")
BACKEND_IP = os.environ.get("BACKEND_IP")
BACKEND_PORT = os.environ.get("BACKEND_PORT")
FRONTEND_IP = os.environ.get("FRONTEND_IP")
FRONTEND_PORT = os.environ.get("FRONTEND_PORT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.environ.get("ALGORITHM")
SECRET_KEY = os.environ.get("SECRET_KEY")


# def get_db_url():
#     return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
#             f"{self.DB_INTERNAL_HOST}:{self.DB_INTERNAL_PORT}/{self.DB_NAME}")


def get_auth_data():
    return {"secret_key": SECRET_KEY, "algorithm": ALGORITHM}

#
# def get_data_for_db_external(self):
#     return {"user": self.DB_USER, "password": self.DB_PASSWORD, "host": self.DB_HOST, "port": self.DB_PORT,
#             "database": self.DB_NAME}


def get_admin_data():
    return {"name": DB_USER, "email": DB_USER + '@mail.ru', "password": DB_PASSWORD}