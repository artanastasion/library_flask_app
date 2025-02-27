from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False)
    publisher = relationship("Publisher", back_populates="books")
    issues = relationship("Issuance", back_populates="book", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book> {self.id} {self.title} {self.author}"

    def to_dict(self, include_issues=True):
        books_dict = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "price": self.price,
            "count": self.count,
            "publisher": self.publisher.to_dict()
        }
        if include_issues:
            books_dict["issues"] = [issues.to_dict() for issues in self.issues]

        return books_dict
