from sqlalchemy import Column, Integer, String, DateTime, Float,UniqueConstraint,Index
from geoalchemy2 import Geometry
from datetime import datetime
from .database import Base
from sqlalchemy.sql.expression import text

class PointData(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        UniqueConstraint("geom"),  # Unique constraint on the geom column
    )

class PolygonData(Base):
    __tablename__ = "polygons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    population_density = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (
        Index("idx_unique_geom", text("ST_AsText(geom)"), unique=True),  # Unique index
    )