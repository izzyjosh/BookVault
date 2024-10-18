from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from api.v1.models.abstract_base_model import AbstractBaseModel
from api.v1.models.book import BookGenreAssociation


class Genre(AbstractBaseModel):
    __tablename__ = "genre"

    name: Mapped[str] = mapped_column(String(50), unique=True)
    books = relationship("Book", secondary=BookGenreAssociation, back_populates="genre")

    def __str__(self):
        return f"{self.name}"
