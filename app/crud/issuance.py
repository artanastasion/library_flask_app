from sqlalchemy.orm import Session
from ..models.issuance import Issuance
from ..models.book import Book
from ..models.reader import Reader
from datetime import date
from sqlalchemy.exc import SQLAlchemyError


def create_issuance(db: Session, reader_id: int, book_id: int, issue_date: date):
    issue_count = db.query(Issuance).filter(Issuance.reader_id == reader_id).count()
    if issue_count >= 5:
        raise ValueError("The permissible number of books for the reader has been exceeded.")

    book = db.query(Book).filter(Book.id == book_id).first()
    reader = db.query(Reader).filter(Reader.id == reader_id).first()

    if not book:
        raise ValueError("Book not found.")
    if not reader:
        raise ValueError("Reader not found.")

    if book.count <= 0:
        raise ValueError("The book is out of stock.")

    issuance = Issuance(
        reader_id=reader_id,
        book_id=book_id,
        issue_date=issue_date
    )

    try:
        book.count -= 1

        db.add(issuance)
        db.commit()
        db.refresh(issuance)
        return issuance
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_issuance(db: Session, issuance_id: int):
    return db.query(Issuance).filter(Issuance.id == issuance_id).first()


def update_issuance(db: Session, issuance_id: int, reader_id: int = None, book_id: int = None, issue_date: date = None):
    issuance = db.query(Issuance).filter(Issuance.id == issuance_id).first()

    if not issuance:
        raise ValueError("Issuance not found.")

    old_book_id = issuance.book_id
    old_book = db.query(Book).filter(Book.id == old_book_id).first()

    new_book = None
    if book_id is not None:
        new_book = db.query(Book).filter(Book.id == book_id).first()
        if not new_book:
            raise ValueError("New book not found.")
        if new_book.count <= 0:
            raise ValueError("The new book is out of stock.")

    try:
        if book_id is not None and book_id != old_book_id:
            old_book.count += 1

            new_book.count -= 1

            issuance.book_id = book_id

        if reader_id is not None:
            issuance.reader_id = reader_id
        if issue_date is not None:
            issuance.issue_date = issue_date

        db.commit()
        db.refresh(issuance)
        return issuance
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_issuance(db: Session, issuance_id: int):
    issuance = db.query(Issuance).filter(Issuance.id == issuance_id).first()
    if issuance:
        try:
            db.delete(issuance)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return issuance


def get_all_issuances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Issuance).offset(skip).limit(limit).all()
