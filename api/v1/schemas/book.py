from pydantic import BaseModel, ConfigDict
from api.v1.schemas.user import BookUserSchema


class AddBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    author: str
    publisher: str
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
