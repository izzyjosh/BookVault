from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from api.v1.schemas.user import UserResponseSchema


# Schema Response
class CreateResponseModel(BaseModel):
    access_token: str
    expiry_time: datetime
    user: UserResponseSchema


class SuccessResponseSchema(BaseModel):
    status_code: int
    message: str
    data: Optional[CreateResponseModel]


# Respinse documentatikn

bad_request = {
    "description": "Bad Request",
    "content": {
        "application/json": {"example": {"status_code": 400, "message": "bad request"}}
    },
}

validation_error = {
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
}

not_found = {
    "description": "Not Found",
    "content": {
        "application/json": {
            "example": {"status_code": 404, "message": "does not exist"}
        }
    },
}


# Responses
register_responses = {
    400: bad_request,
    422: validation_error,
}

login_responses = {
    400: bad_request,
    404: not_found,
    422: validation_error,
}
