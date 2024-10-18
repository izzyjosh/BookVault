from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, func, String
import uuid
from datetime import datetime
from api.v1.utils.database import Base


class AbstractBaseModel(Base):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, index=True, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
