from fastapi import APIRouter, HTTPException, Depends
from geoalchemy2.functions import ST_GeomFromText, ST_AsText, ST_X, ST_Y, ST_SetSRID, ST_MakePoint
from typing import List
from ..schemas.points import PointCreate, PointResponse, PointUpdate
from ..models import PointData
from ..database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
import http.client
from sqlalchemy import exists,and_

router = APIRouter(prefix="/points", tags=["points"])

@router.post("/", response_model=PointResponse,status_code=http.client.CREATED)
async def create_point(point: PointCreate, db: Session = Depends(get_db)):
    try:
         # Check if a point with the same coordinates already exists
        existing_point_exists = db.query(exists().where(
            PointData.geom == ST_SetSRID(ST_MakePoint(point.longitude, point.latitude), 4326)
        )).scalar()

        if existing_point_exists:
            raise HTTPException(
                status_code=http.client.BAD_REQUEST,
                detail="A point with the same coordinates already exists."
            )

        geom = ST_GeomFromText(f"POINT({point.longitude} {point.latitude})", srid=4326)
        db_point = PointData(name=point.name, description=point.description, geom=geom)
        db.add(db_point)
        db.commit()
        db.refresh(db_point)

        point_response = PointResponse(
            id=db_point.id,
            name=db_point.name,
            description=db_point.description,
            longitude=point.longitude,
            latitude=point.latitude,
            geom=str(db.scalar(ST_AsText(db_point.geom))),
            created_at=db_point.created_at,
            updated_at=db_point.updated_at,
        )
        return point_response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error creating point: {e}")


@router.get("/", response_model=List[PointResponse])
def list_points(db: Session = Depends(get_db)):
    try:
        points = db.query(PointData).all()
        point_list = []
        for point in points:
            point_list.append(PointResponse(
                id=point.id,
                name=point.name,
                description=point.description,
                longitude=db.scalar(ST_X(point.geom)),
                latitude=db.scalar(ST_Y(point.geom)),
                geom=str(db.scalar(ST_AsText(point.geom))),
                created_at=point.created_at,
                updated_at=point.updated_at
            ))
        return point_list
    except Exception as e:
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error fetching points: {e}")


@router.put("/{point_id}", response_model=PointResponse)
async def update_point(point_id: int, point_update: PointUpdate, db: Session = Depends(get_db)):
    try:
        db_point = db.query(PointData).filter(PointData.id == point_id).first()

        if not db_point:
            raise HTTPException(status_code=404, detail="Point not found")
         # Check if a point with the same coordinates already exists
        existing_point_exists = db.query(exists().where(and_(
                    PointData.geom == ST_SetSRID(ST_MakePoint(point_update.longitude, point_update.latitude), 4326),
                    PointData.id != point_id  # Exclude the current point from the check
                )
        )).scalar()

        if existing_point_exists:
            raise HTTPException(
                status_code=http.client.BAD_REQUEST,
                detail="A point with the same coordinates already exists."
            )
            
        if point_update.name is not None:
            db_point.name = point_update.name
        if point_update.description is not None:
            db_point.description = point_update.description

        if point_update.longitude is not None and point_update.latitude is not None:
            db_point.geom = ST_SetSRID(ST_MakePoint(point_update.longitude, point_update.latitude), 4326)

        db_point.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_point)

        point_response = PointResponse(
            id=db_point.id,
            name=db_point.name,
            description=db_point.description,
            longitude=db.scalar(ST_X(db_point.geom)),
            latitude=db.scalar(ST_Y(db_point.geom)),
            geom=str(db.scalar(ST_AsText(db_point.geom))),
            created_at=db_point.created_at,
            updated_at=db_point.updated_at,
        )
        return point_response

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=http.client.INTERNAL_SERVER_ERROR, detail=f"Error updating point: {e}")
