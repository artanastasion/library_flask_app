from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from ..models.book import Book


def create_book(db: Session, title: str, author: str, year: int, price: int, count: int, publisher_id: int):
    book = Book(
        title=title,
        author=author,
        year=year,
        price=price,
        count=count,
        publisher_id=publisher_id
    )

    try:
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book_id: int, title: str = None, author: str = None, year: int = None, price: int = None,
                count: int = None, publisher_id: int = None):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if year is not None:
            book.year = year
        if price is not None:
            book.price = price
        if count is not None:
            book.count = count
        if publisher_id is not None:
            book.publisher_id = publisher_id

        try:
            db.commit()
            db.refresh(book)
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return book


def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        try:
            db.delete(book)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    return book


def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Book).offset(skip).limit(limit).all()
