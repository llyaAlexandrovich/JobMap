import uuid
from sqlalchemy import TEXT, Index, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import Mapped, mapped_column, relationship


from tables.database import Base
from tables.models import Vacancy


class SpatialInfo(Base):
    __tablename__  = "spatial_info"
    __table_args__ = (
        Index("idx_spatial_data_geom", "geom", postgresql_using='gist'),
        Index("idx_spatial_data_id", "vacancy_id"),
        {"comment": "QGIS geo-objects table"}
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    location_name: Mapped[str] = mapped_column(TEXT, nullable=False)
    geom: Mapped[WKBElement] = mapped_column(Geometry(geometry_type='MULTIPOLYGON', srid=4326, spatial_index=False), nullable=False, comment="WGS84")
    
    vacancy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vacancies.id", ondelete="CASCADE"))
    vacancy: Mapped["Vacancy"] = relationship(back_populates="spatial_info")
