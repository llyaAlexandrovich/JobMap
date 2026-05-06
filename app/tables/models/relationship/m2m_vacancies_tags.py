import uuid, datetime
from typing import List
from sqlalchemy import TEXT, INTEGER, TIMESTAMP, DateTime, Table, Column, ForeignKey, Index, func
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from tables.database import Base
from tables.models import SpatialInfo


vacancies_tags = Table(
    "vacancies_tags",
    Base.metadata,
    Column("vacancy_id", ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)
