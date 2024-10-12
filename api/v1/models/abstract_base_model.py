from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from pydantic import UUID4
from datetime import datetime


class AbstractBaseModel:
    __abstract__ = True

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True), index=True, primary_key=True, default=lambda: uuid.uuid4()
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
