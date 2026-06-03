import uuid
from datetime import datetime
from sqlalchemy import TEXT, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


from tables.database import Base


class ProvidersInfo(Base):
    __tablename__ = "providers_info"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    provider_name: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    provider_link: Mapped[str] = mapped_column(TEXT)
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
