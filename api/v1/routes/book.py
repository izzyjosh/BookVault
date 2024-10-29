from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.services.book import book_service
from api.v1.models.user import User
from api.v1.schemas.book import AddBookSchema, UpdateBookSchema
from api.v1.responses.success_responses import success_response
from api.v1.docs.schemas import AddBookResponseSchema, add_book_responses


books = APIRouter(prefix="/books", tags=["book"])


@books.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AddBookResponseSchema,
    responses=add_book_responses,
)
async def add_book(
    schema: AddBookSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    response = book_service.add_book(db, user, schema)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Book successfully added",
        data=response,
    )


@books.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=AddBookResponseSchema,
    responses=add_book_responses,
)
async def update_book(
    id: str,
    schema: UpdateBookSchema,
    db: Session = Depends(get_db),
    user: User = Depends(user_service.get_current_user),
):

    response = book_service.update(db, id, user, schema)

    return success_response(message="Book updated successfully", data=response)
