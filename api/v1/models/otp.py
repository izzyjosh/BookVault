from pydantic import UUID4
from datetime import datetime, timedelta
import pyotp
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime
from api.v1.models.abstract_base_model import AbstractBaseModel


class Otp(AbstractBaseModel):
    __tablename__ = "otp"

    code: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    user_id: Mapped[UUID4] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", backref="otpcode")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __str__(self):
        return self.code

    def generate_otp(self):
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, digits=6, interval=30)
        self.code = totp.now()

        self.expires_at = datetime.utcnow() + timedelta(minutes=1440)
