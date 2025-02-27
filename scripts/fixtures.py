import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import issuance, publisher, book, reader

fake = Faker()

engine = create_engine("postgresql+psycopg2://admin1:admin1@localhost:5432/db_library")
Session = sessionmaker(bind=engine)
session = Session()


def generate_publishers(count):
    publishers = []
    for _ in range(count):
        _publisher = publisher.Publisher(
            name=fake.company(),
            city=fake.city()
        )
        publishers.append(_publisher)
    return publishers


def generate_books(count, publishers):
    books = []
    for _ in range(count):
        _book = book.Book(
            title=fake.catch_phrase(),
            author=fake.name(),
            year=random.randint(1900, 2023),
            price=random.randint(5, 100),
            count=random.randint(1, 50),
            publisher_id=random.choice(publishers).id
        )
        books.append(_book)
    return books


def generate_readers(count):
    readers = []
    for _ in range(count):
        _reader = reader.Reader(
            full_name=fake.name(),
            address=fake.address().replace("\n", ", "),
            phone=fake.phone_number()
        )
        readers.append(_reader)
    print(readers)
    return readers


def generate_issues(count, readers, books):
    issues = []
    for _ in range(count):
        _issuance = issuance.Issuance(
            reader_id=random.choice(readers).id,
            book_id=random.choice(books).id,
            issue_date=fake.date_between(start_date='-1y', end_date='today')
        )
        issues.append(_issuance)
    return issues


def main():
    Base.metadata.create_all(engine)

    publishers = generate_publishers(5)
    session.add_all(publishers)
    session.commit()

    publishers = session.query(publisher.Publisher).all()
    books = generate_books(10, publishers)
    session.add_all(books)
    session.commit()

    readers = generate_readers(10)
    session.add_all(readers)
    session.commit()

    books = session.query(book.Book).all()
    issues = generate_issues(20, readers, books)
    session.add_all(issues)

    session.commit()
    session.close()


if __name__ == '__main__':
    main()
