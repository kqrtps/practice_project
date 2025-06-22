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

@router.post("/advertisements/", response_model=schemas.AdvertisementRead, status_code=201)
def create_ad(ad: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.create_advertisement(db, ad)

@router.get("/advertisements/", response_model=list[schemas.AdvertisementRead])
def read_ads(db: Session = Depends(get_db)):
    return crud.get_advertisements(db)

@router.get("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def read_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.get_advertisement(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad

@router.put("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def update_ad(ad_id: int, ad_data: schemas.AdvertisementUpdate, db: Session = Depends(get_db)):
    updated = crud.update_advertisement(db, ad_id, ad_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return updated

@router.delete("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_advertisement(db, ad_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return deleted
