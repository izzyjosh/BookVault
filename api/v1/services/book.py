from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from api.v1.schemas.book import AddBookSchema
from api.v1.models.book import Book
from api.v1.models.user import User
from api.v1.models.genre import Genre
from api.v1.models.category import Category
from api.v1.utils.storage import upload
from api.v1.schemas.book import BookResponseSchema


class BookService:

    def get_detailed_book(self, db: Session, id: str):
        book = (
            db.query(Book)
            .options(
                joinedload(Book.genre),
                joinedload(Book.category),
            )
            .filter(Book.id == id)
            .first()
        )

        return jsonable_encoder(book)

    def add_book(self, db: Session, user: User, schema: AddBookSchema):

        if user.role == "member":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="you do not have the permission to add book",
            )

        schema_dict = schema.model_dump()
        total_copies = schema_dict.pop("total_copies")
        genre = schema_dict.pop("genre")
        categoryName = schema_dict.pop("category")
        image = schema_dict.pop("image")

        book = Book(**schema_dict)

        # upload image for storage
        image = upload(image)
        book.image = image

        book.update_copies(total_copies)

        # add genre
        for name in genre:
            genre = db.query(Genre).filter(Genre.name == name).first()

            if not genre:
                genre = Genre(name=name)

                db.add(genre)
            book.genre.append(genre)

        # category check
        category = db.query(Category).filter(Category.name == categoryName).first()

        if not category:
            category = Category(name=categoryName)
            db.add(category)
        book.category = category

        db.add(book)
        db.commit()
        db.refresh(book)

        return BookResponseSchema(
            **jsonable_encoder(book), category=categoryName, genre=schema.genre
        )


book_service = BookService()
