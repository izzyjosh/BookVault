from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import APIRouter, status, Depends
from api.v1.services.user import user_service
from api.v1.schemas.user import UserUpdateSchema, UserResponseSchema
from api.v1.models.user import User
from api.v1.utils.dependencies import get_db
from api.v1.docs.schemas import (
    SuccessResponseSchema,
    update_responses,
    delete_responses,
)
from api.v1.responses.success_responses import success_response

users = APIRouter(prefix="/users", tags=["user"])


@users.patch(
    "/{id}",
    response_model=SuccessResponseSchema,
    status_code=status.HTTP_200_OK,
    responses=update_responses,
)
async def update_user(
    id: UUID4,
    schema: UserUpdateSchema,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    response = user_service.update(db, schema, user, id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User Updated successfully",
        data=response,
    )


@users.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, responses=delete_responses
)
async def delete_user(
    id: UUID4,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):

    user_service.delete_user(db, id, user)

    return success_response(
        status_code=status.HTTP_204_NO_CONTENT,
        message="User deleted successfully",
    )
