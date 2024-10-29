from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Integer, ForeignKey, Table, Column, ARRAY, JSON
from sqlalchemy.ext.mutable import MutableList
from api.v1.models.abstract_base_model import AbstractBaseModel
from api.v1.schemas.user import BookUserSchema
from api.v1.utils.database import Base
from datetime import datetime, timedelta

BookGenreAssociation = Table(
    "genreAssociation",
    Base.metadata,
    Column(
        "genre_id", String, ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "book_id", String, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True
    ),
)

BookUserAssociation = Table(
    "bookUserAssociation",
    Base.metadata,
    Column(
        "user_id", String, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "book_id", String, ForeignKey("book.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Book(AbstractBaseModel):
    __tablename__ = "book"

    title: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    authors: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String(50)))
    )
    publishers: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String(100)))
    )
    image: Mapped[str] = mapped_column(String(1024))
    year: Mapped[int]
    isbn: Mapped[str] = mapped_column(String, unique=True)
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))
    category = relationship("Category", back_populates="books")
    genre: Mapped[list[str]] = relationship(
        "Genre",
        secondary=BookGenreAssociation,
        back_populates="books",
        cascade="save-update, merge",
    )
    copies_available: Mapped[int] = mapped_column(default=0, nullable=False)
    total_copies: Mapped[int] = mapped_column(default=0)
    borrowers: Mapped[list[dict]] = mapped_column(
        MutableList.as_mutable(ARRAY(JSON)), nullable=True
    )
    reservation_queue: Mapped[list["User"]] = relationship(
        "User", secondary=BookUserAssociation, back_populates="queued_users"
    )
    history: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)), nullable=True, default=[]
    )
    fine_details: Mapped[dict[str, int]] = mapped_column(
        JSON, default={}, nullable=True
    )

    # Model methods

    def update_copies(self, num_copies: int):
        if self.copies_available is None:
            self.copies_available = 0
        if self.total_copies is None:
            self.total_copies = 0
        self.copies_available += num_copies
        self.total_copies += num_copies

    @property
    def is_available(self):
        return self.copies_available > 0

    def reserve_book(self, user: BookUserSchema):
        if not self.is_available():
            self.reservation_queue.append(user)
            return True
        else:
            return False

    def borrow_book(self, user: BookUserSchema):
        if self.is_available():
            self.copies_available -= 1
            self.borrowers.append({"user": user, "due_date": self.calculate_due_date()})

            return f"{user.username} borrowed {self.title}"
        else:
            self.reserve_book(user)
            return f"{self.title} not available for borrowing. {self.user} added to reservation"

    def return_book(self, user: BookUserSchema):
        if any(borrower[user] == user for borrower in self.borrowers):
            self.copies_available += 1
            self.borrowers = [
                borrower for borrower in self.borrowers if borrower[user] != user
            ]

            return f"{user.username} returned {self.title}"
        else:
            return f"{user.username} did not borrow this book"

    def calculate_due_date(self):
        return datetime.now() + timedelta(days=14)
