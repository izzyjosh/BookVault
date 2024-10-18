from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from api.v1.models.abstract_base_model import AbstractBaseModel


class Category(AbstractBaseModel):
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    books = relationship("Book", back_populates="category", cascade="all, delete")

    def __str__(self):
        return f"{self.name}"
