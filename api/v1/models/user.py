from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Enum as SQLAlchemyEnum, func, Boolean, DateTime
from api.v1.models.abstract_base_model import AbstractBaseModel
from pydantic import EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime


class Role(Enum):
    admin = "admin"
    liberian = "liberian"
    member = "member"


class User(AbstractBaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        String(50),
        index=True,
    )
    first_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    reg_number: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    email: Mapped[EmailStr] = mapped_column(String(225), index=True)
    password: Mapped[str] = mapped_column(String(1024))
    bio: Mapped[Optional[str]] = mapped_column(String(1024))
    role: Mapped[str] = mapped_column(SQLAlchemyEnum(Role), default=Role.member)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}: @{self.username}"
