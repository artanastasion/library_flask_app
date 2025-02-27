from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Reader(Base):
    __tablename__ = "readers"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    issues = relationship("Issuance", back_populates="reader", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Reader> {self.id} {self.full_name}"

    def to_dict(self, include_issues=True):
        reader_dict = {
            "id": self.id,
            "full_name": self.full_name,
            "address": self.address,
            "phone": self.phone
        }
        if include_issues:
            reader_dict["issues"] = [issues.to_dict() for issues in self.issues]
        return reader_dict
