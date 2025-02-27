import os

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql+psycopg2://{USERNAME_DB}:{PASSWORD_DB}@localhost:5432/{NAME_DB}")


class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
