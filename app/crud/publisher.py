from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.publisher import Publisher


def create_publisher(db: Session, name: str, city: str):
    publisher = Publisher(
        name=name,
        city=city
    )

    try:
        db.add(publisher)
        db.commit()
        db.refresh(publisher)
        return publisher
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_publisher(db: Session, publisher_id: int):
    return db.query(Publisher).filter(Publisher.id == publisher_id).first()


def update_publisher(db: Session, publisher_id: int, name: str = None, city: str = None):
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if publisher:
        if name is not None:
            publisher.name = name
        if city is not None:
            publisher.city = city
        try:
            db.commit()
            db.refresh(publisher)
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return publisher


def delete_publisher(db: Session, publisher_id: int):
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if publisher:
        try:
            db.delete(publisher)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return publisher


def get_all_publishers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Publisher).offset(skip).limit(limit).all()
