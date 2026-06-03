from typing import List
from sqlalchemy import TEXT, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship


from tables.database import Base
from tables.models.relationship.m2m_vacancies_tags import vacancies_tags


class Tag(Base):
    __tablename__  = "tags"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    tag_name: Mapped[str] = mapped_column(TEXT, unique=True, nullable=False)
    tag_count: Mapped[int] = mapped_column(BIGINT, default=0)

    vacancies_rel: Mapped[List["Vacancy"]] = relationship(secondary=vacancies_tags, back_populates="tags_rel")
