import uuid
from sqlalchemy import TEXT, Integer, Boolean, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


from tables.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (Index("idx_users_id", "id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, server_default=func.gen_random_uuid())
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    rights: Mapped[int] = mapped_column(Integer, default=1)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False, unqique=True)
    telegram_name: Mapped[str] = mapped_column(TEXT)
    email: Mapped[str] = mapped_column(TEXT, unique=True)
    phone_number: Mapped[str] = mapped_column(TEXT, unique=True)
