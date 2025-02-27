import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin1:admin1@localhost:5432/db_library")


class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
