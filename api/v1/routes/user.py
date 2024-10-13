from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from api.v1.schemas.user import UserCreateSchema, LoginSchema
from api.v1.docs.schemas import (
    SuccessResponseSchema,
    register_responses,
    login_responses,
)
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.responses.success_responses import success_response

accounts = APIRouter(prefix="/account", tags=["account"])


@accounts.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponseSchema,
    responses=register_responses,
)
async def create_user(schema: UserCreateSchema, db: Session = Depends(get_db)):

    response = user_service.create_user(db=db, schema=schema)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=response,
    )


@accounts.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=SuccessResponseSchema,
    responses=login_responses,
)
async def login(data: LoginSchema, db: Session = Depends(get_db)):
    response = user_service.handle_login(
        db=db, email=data.email, password=data.password
    )

    return success_response(
        status_code=status.HTTP_200_OK, message="Login successfully", data=response
    )
