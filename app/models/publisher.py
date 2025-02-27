from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    books = relationship("Book", back_populates="publisher", cascade="all, delete-orphan", uselist=True)

    def __repr__(self):
        return f"<Publisher> {self.id} {self.name} {self.books}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
        }
