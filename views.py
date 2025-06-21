from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db

router = APIRouter()

@router.get("/locations/{location_id}", response_model=schemas.LocationRead)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router.get("/locations/", response_model=list[schemas.LocationRead])
def read_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)


@router.put("/locations/{location_id}", response_model=schemas.LocationRead)
def put_location(location_id: int, location: schemas.LocationUpdate,db: Session = Depends(get_db)):
    updated_location = crud.update_location(db, location_id, location.location_name)
    if updated_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated_location
@router.post("/locations/", response_model=schemas.LocationRead, status_code=201)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, location)

@router.delete("/locations/{location_id}", response_model=schemas.LocationRead)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    deleted_location = crud.delete_location(db, location_id)
    if deleted_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return deleted_location

