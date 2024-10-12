from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Boolean
from pydantic import UUID4
from api.v1.models.abstract_base_model import AbstractBaseModel
from datetime import datetime


class AccessToken(AbstractBaseModel):

    __tablename__ = "access_token"

    user_id: Mapped[UUID4] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", backref="access_token")
    token: Mapped[str] = mapped_column(String(2048))
    expiry_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    blacklisted: Mapped[bool] = mapped_column(
        Boolean(), server_default="false", default=False
    )

    def __repr__(self) -> str:
        return self.token
