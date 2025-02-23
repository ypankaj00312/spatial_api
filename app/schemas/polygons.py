from pydantic import BaseModel
from typing import Optional, List, Tuple
from datetime import datetime

# Pydantic models for request and response bodies
class PolygonCreate(BaseModel):
    name: str
    description: Optional[str] = None
    coordinates: List[Tuple[float, float]]
    population_density: Optional[float] = None

class PolygonResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    geom: Optional[str]
    population_density: Optional[float]
    created_at: datetime
    updated_at: datetime

class PolygonUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    coordinates: Optional[List[Tuple[float, float]]] = None
    population_density: Optional[float] = None