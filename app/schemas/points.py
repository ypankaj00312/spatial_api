from pydantic import BaseModel
from typing import Optional, Tuple
from datetime import datetime

# Pydantic models for request and response bodies
class PointCreate(BaseModel):
    name: str
    description: Optional[str] = None
    longitude: float
    latitude: float

class PointResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    longitude: float
    latitude: float
    geom: Optional[str]  # WKT representation
    created_at: datetime
    updated_at: datetime

class PointUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None