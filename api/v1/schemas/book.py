from pydantic import BaseModel, ConfigDict
from api.v1.schemas.user import BookUserSchema
from typing import Optional


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


class UpdateBookSchema(AddBookSchema):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str]
    authors: list[str] | None = None
    publishers: list[str] | None = None
    image: str | None = None
    year: int | None = None
    isbn: str | None = None
    total_copies: int | None = None
