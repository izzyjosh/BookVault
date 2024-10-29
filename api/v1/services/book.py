from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from api.v1.schemas.book import AddBookSchema, BookResponseSchema, UpdateBookSchema
from api.v1.models.book import Book
from api.v1.models.user import User
from api.v1.models.genre import Genre
from api.v1.models.category import Category
from api.v1.utils.storage import upload


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

    def get_by_isbn(self, db: Session, isbn: str) -> bool:
        book = db.query(Book).filter(Book.isbn == isbn).first()

        if book:
            return True
        return False

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
        isbn = schema_dict.pop("isbn")

        if not self.get_by_isbn(db, isbn):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with the isbn already exist",
            )

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

    def update(self, db: Session, book_id: str, user: User, schema: UpdateBookSchema):

        schema_dict = schema.model_dump()
        genre = schema_dict.pop("genre")
        categoryName = schema_dict.pop("category")
        total_copies = schema_dict.pop("total_copies")

        book = db.query(Book).filter(Book.id == book_id).first()

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book does not exist"
            )

        for key, value in schema_dict.items():
            if hasattr(book, key):
                setattr(book, key, value)

        # update book copies
        book.update_copies(total_copies)

        # add genre
        for name in genre:
            genre = db.query(Genre).filter(Genre.name == name).first()
            if not genre:
                genre = Genre(name=name)
                db.add(genre)

            if genre not in book.genre:
                book.genre.append(genre)

        category = db.query(Category).filter(Category.name == categoryName).first()

        if not category:
            category = Category(name=categoryName)
            db.add(category)
        book.category = category

        db.commit()
        db.refresh(book)

        return BookResponseSchema(
            **jsonable_encoder(book),
            category=category.name,
            genre=[genre.name for genre in book.genre]
        )


book_service = BookService()
