import uuid, datetime
from typing import List
from sqlalchemy import TEXT, INTEGER, SMALLINT, TIMESTAMP, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tables.database import Base
from tables.models import SpatialInfo
from tables.models import Tag
from tables.models.relationship.m2m_vacancies_tags import vacancies_tags


class Vacancy(Base):
    __tablename__  = "vacancies"
    __table_args__ = (Index("idx_vacancies_id", "id"),)

    id: Mapped[uuid.UUID]         = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    vacancy_name: Mapped[str]     = mapped_column(TEXT, nullable=False)
    vacancy_type: Mapped[int]     = mapped_column(INTEGER, nullable=False)
    vacancy_link: Mapped[str]     = mapped_column(TEXT, nullable=True)
    created_at: Mapped[DateTime]  = mapped_column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    visibility: Mapped[int]       = mapped_column(SMALLINT, default=0)
    tags_array: Mapped[List[str]] = mapped_column("tags", ARRAY(TEXT), nullable=True)
    hash: Mapped[str]             = mapped_column(TEXT, unique=True, nullable=False)

    spatial_info: Mapped[List["SpatialInfo"]] = relationship(back_populates="vacancy", cascade="all, delete-orphan")
    tags: Mapped[List["Tag"]] = relationship(secondary=vacancies_tags, back_populates="vacancies")
