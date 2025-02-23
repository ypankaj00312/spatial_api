from fastapi import APIRouter, HTTPException, Depends
from geoalchemy2.functions import ST_GeomFromText, ST_AsText, ST_Equals, ST_SetSRID
from typing import List
from ..schemas.polygons import PolygonCreate, PolygonResponse, PolygonUpdate
from ..models import PolygonData
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
import http.client
from sqlalchemy import exists,and_

router = APIRouter(prefix="/polygons", tags=["polygons"])

@router.post("/", response_model=PolygonResponse,status_code=http.client.CREATED)
async def create_polygon( polygon: PolygonCreate, db: Session = Depends(get_db)):
    try:  
        coordinates_str = ",".join([f"{coord[0]} {coord[1]}" for coord in polygon.coordinates])
        geom = ST_GeomFromText(f"POLYGON(({coordinates_str}))", srid=4326)
        
        # # Check if a polygon with the same geometry already exists
        existing_polygon_exists = db.query(
        exists().where(
        ST_Equals(PolygonData.geom, ST_SetSRID(geom, 4326))
        )
        ).scalar()


        if existing_polygon_exists:
            raise HTTPException(
                status_code=400,
                detail="A polygon with the same coordinates already exists."
            )
            
        db_polygon = PolygonData(name=polygon.name, description=polygon.description, geom=geom, population_density=polygon.population_density)
        db.add(db_polygon)
        db.commit()
        db.refresh(db_polygon)

        polygon_response = PolygonResponse(
            id=db_polygon.id,
            name=db_polygon.name,
            description=db_polygon.description,
            geom=str(db.scalar(ST_AsText(db_polygon.geom))),
            population_density=db_polygon.population_density,
            created_at=db_polygon.created_at,
            updated_at=db_polygon.updated_at,
        )

        return polygon_response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error creating polygon: {e}")

@router.get("/", response_model=List[PolygonResponse])
def list_polygons(db: Session = Depends(get_db)):
    try:
        polygons = db.query(PolygonData).all()
        polygon_list = []
        for polygon in polygons:
            polygon_list.append(PolygonResponse(
                id=polygon.id,
                name=polygon.name,
                description=polygon.description,
                geom=str(db.scalar(ST_AsText(polygon.geom))),
                population_density=polygon.population_density,
                created_at=polygon.created_at,
                updated_at=polygon.updated_at
            ))
        return polygon_list
    except Exception as e:
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error fetching polygons: {e}")

@router.put("/{polygon_id}", response_model=PolygonResponse)
async def update_polygon(polygon_id: int, polygon_update: PolygonUpdate, db: Session = Depends(get_db)):
    try:  
        db_polygon = db.query(PolygonData).filter(PolygonData.id == polygon_id).first()

        if not db_polygon:
            raise HTTPException(status_code=404, detail="Polygon not found")
        
        if polygon_update.coordinates is not None:
            coordinates_str = ",".join([f"{coord[0]} {coord[1]}" for coord in polygon_update.coordinates])
            new_geom = ST_GeomFromText(f"POLYGON(({coordinates_str}))", srid=4326)

            # Check if a polygon with the same geometry already exists
            existing_polygon_exists = db.query(
                exists().where(
                    ST_Equals(PolygonData.geom, ST_SetSRID(new_geom, 4326)),
                    PolygonData.id != polygon_id  # Exclude the current polygon from the check
                )
            ).scalar()

            if existing_polygon_exists:
                raise HTTPException(
                    status_code=400,
                    detail="A polygon with the same coordinates already exists."
                )
            
            db_polygon.geom = new_geom

        if polygon_update.name is not None:
            db_polygon.name = polygon_update.name
        if polygon_update.description is not None:
            db_polygon.description = polygon_update.description

        if polygon_update.coordinates is not None:
            coordinates_str = ",".join([f"{coord[0]} {coord[1]}" for coord in polygon_update.coordinates])
            db_polygon.geom = ST_GeomFromText(f"POLYGON(({coordinates_str}))", srid=4326)

        if polygon_update.population_density is not None:
            db_polygon.population_density = polygon_update.population_density

        db_polygon.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_polygon)

        polygon_response = PolygonResponse(
            id=db_polygon.id,
            name=db_polygon.name,
            description=db_polygon.description,
            geom=str(db.scalar(ST_AsText(db_polygon.geom))),
            population_density=db_polygon.population_density,
            created_at=db_polygon.created_at,
            updated_at=db_polygon.updated_at,
        )
        return polygon_response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error updating polygon: {e}")
