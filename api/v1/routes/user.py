from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from api.v1.schemas.user import UserCreateSchema
from api.v1.docs.schemas import SuccessResponseSchema, responses
from api.v1.utils.dependencies import get_db
from api.v1.services.user import user_service
from api.v1.responses.success_responses import success_response

accounts = APIRouter(prefix="/account", tags=["account"])


@accounts.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponseSchema,
    responses=responses,
)
async def create_user(schema: UserCreateSchema, db: Session = Depends(get_db)):

    response = user_service.create_user(db=db, schema=schema)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=response,
    )
