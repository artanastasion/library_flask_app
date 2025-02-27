from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.reader import Reader


def create_reader(db: Session, full_name: str, address: str, phone: str):
    reader = Reader(
        full_name=full_name,
        address=address,
        phone=phone
    )
    try:
        db.add(reader)
        db.commit()
        db.refresh(reader)

        return reader
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_reader(db: Session, reader_id: int):
    return db.query(Reader).filter(Reader.id == reader_id).first()


def update_reader(db: Session, reader_id: int, full_name: str = None, address: str = None, phone: str = None):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader:
        if full_name is not None:
            reader.full_name = full_name
        if address is not None:
            reader.address = address
        if phone is not None:
            reader.phone = phone

        try:
            db.commit()
            db.refresh(reader)
            return reader
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return reader


def delete_reader(db: Session, reader_id: int):
    reader = db.query(Reader).filter(Reader.id == reader_id).first()
    if reader:
        try:
            db.delete(reader)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return reader


def get_all_readers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reader).offset(skip).limit(limit).all()
