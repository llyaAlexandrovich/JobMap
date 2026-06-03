import uuid
from typing import List
from sqlalchemy import TEXT, Index, func
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column, relationship


from tables.database import Base


class SpatialInfo(Base):
    __tablename__  = "spatial_info"
    __table_args__ = (
        Index("idx_spatial_data_geom", "geom", postgresql_using='gist'),
        {"comment": "QGIS geo-objects table"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    location_name: Mapped[str] = mapped_column(TEXT, nullable=False)
    geom: Mapped[WKBElement] = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True), nullable=False, comment="WGS84")

    vacancies: Mapped[List["Vacancy"]] = relationship(back_populates="spatial_rel")
    companies: Mapped[List["CompanyInfo"]] = relationship(back_populates="location_rel")
