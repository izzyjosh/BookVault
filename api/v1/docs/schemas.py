from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from api.v1.schemas.user import UserResponseSchema


class CreateResponseModel(BaseModel):
    access_token: str
    expiry_time: datetime
    user: UserResponseSchema


class SuccessResponseSchema(BaseModel):
    status_code: int = 201
    message: str
    data: Optional[CreateResponseModel]


responses = {
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "string"}}},
    },
    422: {
        "description": "Validation Error",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 422,
                    "message": "Validation errors",
                    "errors": [{"field_name": "field error message"}],
                }
            }
        },
    },
}
