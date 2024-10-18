from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from api.v1.schemas.user import UserResponseSchema
from api.v1.schemas.book import BookResponseSchema


# Schema Response
class CreateResponseModel(BaseModel):
    access_token: str
    expiry_time: datetime
    user: UserResponseSchema


class SuccessResponseSchema(BaseModel):
    status_code: int
    message: str
    data: Optional[CreateResponseModel]


class VerifyResponseSchema(BaseModel):
    status_code: int = 200
    message: str
    data: UserResponseSchema


class AddBookResponseSchema(BaseModel):
    status_code: int = 201
    message: str
    data: BookResponseSchema


class GetUsersResponse(BaseModel):
    status_code: int = 200
    message: str
    data: list[UserResponseSchema]


# Response documentatikn

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
forbidden = {
    "description": "Forbidden",
    "content": {
        "application/json": {
            "example": {"status_code": 403, "message": "Do not have the permission"}
        }
    },
}
not_authorized = {
    "description": "Unauthorized",
    "content": {
        "application/json": {
            "example": {"status_code": 401, "message": "not authorized"}
        }
    },
}
no_content = {
    "description": "No Content",
    "content": {
        "application/json": {
            "example": {"status_code": 204, "message": "No content, already deleted"}
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
email_verify_responses = {
    400: bad_request,
    422: validation_error,
}
update_responses = {403: forbidden, 422: validation_error, 401: not_authorized}

admin_update_responses = {401: not_authorized, 403: forbidden, 422: validation_error}

get_users_responses = {401: not_authorized, 403: forbidden}

delete_responses = {
    204: no_content,
    404: not_found,
    422: validation_error,
}

# book docs
add_book_responses = {401: not_authorized, 403: forbidden, 422: validation_error}
