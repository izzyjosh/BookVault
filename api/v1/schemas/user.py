from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str = Field(..., example="adstra")
    email: EmailStr
    first_name: str | None = Field(default=None, example="Joshua")
    last_name: str | None = Field(default=None, example="Joseph")
    bio: str | None = None
    reg_number: str | None = Field(default=None, example="U22AE1077")
    role: str = Field(example="member")
    last_login: datetime | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LoginSchema(BaseModel):
    model_config = ConfigDict(from_attribute=True)

    email: EmailStr
    password: str


class EmailVerificationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: int


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    reg_number: Optional[str]
    bio: Optional[str]


class BookUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
