from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
