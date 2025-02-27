from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Issuance(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    issue_date = Column(Date, nullable=False)
    reader = relationship("Reader", back_populates="issues", uselist=False)
    book = relationship("Book", back_populates="issues", uselist=False)

    def __repr__(self):
        return f"<Issuance> {self.id} {self.reader_id} {self.book_id}"

    def to_dict(self):
        return {
            "id": self.id,
            "reader_id": self.reader_id,
            "book_id": self.book_id,
            "issue_date": self.issue_date
        }
