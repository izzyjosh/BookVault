from pydantic import BaseModel, ConfigDict
from api.v1.schemas.user import BookUserSchema
from typing import Optional
from api.v1.models.book import Book


class AddBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    authors: list[str]
    publishers: list[str]
    image: str
    year: int
    genre: list[str] | None = None
    isbn: str
    category: str | None = None
    total_copies: int


class BookResponseSchema(AddBookSchema):
    model_config = ConfigDict(from_attributes=True)

    id: str
    copies_available: int
    borrowers: list[dict] | None = None
    reservation_queue: list[BookUserSchema] | None = None
    history: list[str] | None = None
    fine_details: dict[str, int] | None = None

    @classmethod
    def book_payload(cls, book: Book):
        return cls(
            id=book.id,
            title=book.title,
            authors=book.authors,
            publishers=book.publishers,
            image=book.image,
            year=book.year,
            genre=[genre.name for genre in book.genre],
            isbn=book.isbn,
            category=book.category.name,
            total_copies=book.total_copies,
            copies_available=book.copies_available,
        )


class UpdateBookSchema(AddBookSchema):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str]
    authors: list[str] | None = None
    publishers: list[str] | None = None
    image: str | None = None
    year: int | None = None
    isbn: str | None = None
    total_copies: int | None = None
