import os

from dotenv import load_dotenv

load_dotenv()


APP_HOST = os.getenv("APP_HOST", "localhost")
APP_PORT = int(os.getenv("APP_PORT", 8000))

DB_USER = os.getenv("DATABASE_USER", "postgres")
DB_PASS = os.getenv("DATABASE_PASSWORD", "postgres")
DB_NAME = os.getenv("DATABASE_NAME", "postgres")
DB_PORT = int(os.getenv("DATABASE_PORT", 2345))
DB_HOST = os.getenv("DATABASE_HOST", "0.0.0.0")
DB_DRIVER = os.getenv("DATABASE_DRIVER", "asyncpg")
DB_DIALECT = os.getenv("DATABASE_DIALECT", "postgresql")


DB_URL = (
    f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
