import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.book import Book
from app.models.publisher import Publisher
from app.crud.book import create_book, get_book, update_book, delete_book, get_all_books
from app.database import Base


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(f"postgresql+psycopg2://{NANE_TEST_DB}:{PASSWORD_TEST_DB}@localhost:5432/{NAME_TEST_DB}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    session.close()


@pytest.fixture
def test_publisher(db_session):
    publisher = Publisher(
        name="Test Publisher",
        city="Test City"
    )
    db_session.add(publisher)
    db_session.commit()
    return publisher


@pytest.fixture
def test_book(db_session, test_publisher):
    book = Book(
        title="Test Book",
        author="Test Author",
        year=2021,
        price=100,
        count=10,
        publisher_id=test_publisher.id
    )
    db_session.add(book)
    db_session.commit()
    return book


def test_create_book(db_session, test_publisher):
    book_data = {
        "title": "New Book",
        "author": "New Author",
        "year": 2022,
        "price": 200,
        "count": 5,
        "publisher_id": test_publisher.id
    }
    book = create_book(db_session, **book_data)
    assert book.id is not None
    assert book.title == "New Book"
    assert book.author == "New Author"
    assert book.year == 2022
    assert book.price == 200
    assert book.count == 5
    assert book.publisher_id == test_publisher.id


def test_get_book(db_session, test_book):
    book = get_book(db_session, test_book.id)
    assert book.id == test_book.id
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.year == 2021
    assert book.price == 100
    assert book.count == 10
    assert book.publisher_id == test_book.publisher_id


def test_update_book(db_session, test_book, test_publisher):
    updated_book = update_book(
        db_session,
        test_book.id,
        title="Updated Title",
        author="Updated Author",
        year=2023,
        price=150,
        count=20,
        publisher_id=test_publisher.id
    )
    assert updated_book.title == "Updated Title"
    assert updated_book.author == "Updated Author"
    assert updated_book.year == 2023
    assert updated_book.price == 150
    assert updated_book.count == 20
    assert updated_book.publisher_id == test_publisher.id


def test_delete_book(db_session, test_book):
    deleted_book = delete_book(db_session, test_book.id)
    assert deleted_book.id == test_book.id
    assert get_book(db_session, test_book.id) is None


def test_get_all_books(db_session, test_book):
    book2 = Book(
        title="Another Book",
        author="Another Author",
        year=2023,
        price=300,
        count=15,
        publisher_id=test_book.publisher_id
    )
    db_session.add(book2)
    db_session.commit()

    books = get_all_books(db_session)

    assert len(books) == 2
    assert books[0].id == test_book.id
    assert books[1].id == book2.id