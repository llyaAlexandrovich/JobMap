import uuid
from typing import Optional
from sqlalchemy import TEXT, SMALLINT, Index, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from tables.database import Base


class CompanyInfo(Base):
    __tablename__ = "companies_info"
    __table_args__ = (Index("idx_companies_info_id", "id"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    company_name: Mapped[str] = mapped_column(TEXT, nullable=False, unique=True)
    company_location: Mapped[uuid.UUID] = mapped_column(ForeignKey("spatial_info.id", ondelete="CASCADE"))
    company_link: Mapped[Optional[str]] = mapped_column(TEXT)
    company_rating: Mapped[int] = mapped_column(SMALLINT, default=100)

    location_rel: Mapped["SpatialInfo"] = relationship(back_populates="companies")
