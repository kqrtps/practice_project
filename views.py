from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from .models import User
from .dependencies import get_current_user
router = APIRouter()
router_user = APIRouter()
router_ad=APIRouter()

#Location

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


#User

@router_user.get("/user/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int , db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router_user.post("/user", response_model=schemas.UserRead,status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return schemas.UserRead.model_validate(db_user)

@router_user.put("/user/{user_id}", response_model=schemas.UserRead)
def update_user(user_id:int ,user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserRead.model_validate(updated_user)

@router_user.delete("/user/{user_id}", response_model=schemas.UserRead)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserRead.model_validate(deleted_user)


@router_ad.post("/advertisements/", response_model=schemas.AdvertisementRead, status_code=201)
def create_ad(
        ad: schemas.AdvertisementCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    ad.user_id = current_user.user_id  # 💡 юзер не може підставити чужий user_id
    return crud.create_advertisement(db, ad)


@router_ad.get("/advertisements/", response_model=list[schemas.AdvertisementRead])
def read_ads(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    all_ads = crud.get_advertisements(db)
    return [ad for ad in all_ads if ad.location_id == current_user.location_id]


@router_ad.get("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def read_ad(
        ad_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad or ad.location_id != current_user.location_id:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad


@router_ad.put("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def update_ad(
        ad_id: int,
        ad_data: schemas.AdvertisementUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad or ad.location_id != current_user.location_id:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    updated = crud.update_advertisement(db, ad_id, ad_data)
    return updated


@router_ad.delete("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def delete_ad(
        ad_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad or ad.location_id != current_user.location_id:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    deleted = crud.delete_advertisement(db, ad_id)
    return deleted

