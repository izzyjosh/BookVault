from sqlalchemy.orm import Session
from pydantic import UUID4
from fastapi import APIRouter, status, Depends
from api.v1.utils.dependencies import get_db
from api.v1.models.user import User
from api.v1.services.user import user_service
from api.v1.services.admin import admin_service
from api.v1.services.book import book_service
from api.v1.schemas.admin import AdminUpdateSchema
from api.v1.responses.success_responses import success_response
from api.v1.docs.schemas import (
    SuccessResponseSchema,
    admin_update_responses,
    GetUsersResponse,
    get_users_responses,
)

admin = APIRouter(prefix="/admin", tags=["admin"])


@admin.get(
    "/users",
    status_code=status.HTTP_200_OK,
    response_model=GetUsersResponse,
    responses=get_users_responses,
)
async def get_users(
    db: Session = Depends(get_db), user: User = Depends(admin_service.update_role)
):

    response = admin_service.fetch_users(db)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User returned successfully",
        data=response,
    )


@admin.patch(
    "/{id}",
    summary="Admin update user",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponseSchema,
    responses=admin_update_responses,
)
async def update_user_role(
    id: str,
    schema: AdminUpdateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(admin_service.update_role),
):

    response = user_service.update(db, schema, user, id)

    return success_response(
        status_code=status.HTTP_200_OK, message="Updated successfully", data=response
    )


# Admin remove book
@admin.delete("/{id}}", summary="Admin delete book")
async def delete_book(
    id: str,
    db: Session = Depends(get_db),
    user: User = Depends(admin_service.update_role),
):

    book_service.remove(db, id, user)

    return success_response(message="Book remove siccessfully")
