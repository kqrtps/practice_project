from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import crud
from crud import get_current_user
import schemas
import services
from database import get_db
from models import User, Location
from typing import Optional

router_location = APIRouter()
router_user = APIRouter()
router_ad = APIRouter()
router_login = APIRouter()
router_r = APIRouter()

# ------------------- Location -------------------

@router_location.get("/locations/{location_id}", response_model=schemas.LocationRead)
def read_location(location_id: int, db: Session = Depends(get_db)):
    db_location = crud.get_location(db, location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@router_location.get("/locations/", response_model=list[schemas.LocationRead])
def read_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)

@router_location.put("/locations/{location_id}", response_model=schemas.LocationRead)
def put_location(
    location_id: int,
    location: schemas.LocationUpdate,
    current_user: User = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    if db_location.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this location")

    updated_location = crud.update_location(db, location_id, location.location_name)
    return updated_location

@router_location.post("/locations/", response_model=schemas.LocationRead, status_code=201)
def create_location(
    location: schemas.LocationCreate,
    current_user: User = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_location(db, location, current_user.user_id)

@router_location.delete("/locations/{location_id}", response_model=schemas.LocationRead)
def delete_location(
    location_id: int,
    current_user: User = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    if db_location.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this location")
    deleted_location = crud.delete_location(db, location_id)
    return deleted_location

# ------------------- User -------------------

@router_r.post("/register", response_model=schemas.UserRead, summary="Реєстрація користувача з локацією", description="Створює нового користувача і пов'язує його з новою локацією. Локація створюється автоматично.")
def register(user: schemas.UserCreateWithLocation, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = crud.create_user_with_location(
        db, user.username, user.password, user.location_name
    )
    return new_user

@router_user.get("/user/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router_user.post("/user/", response_model=schemas.UserRead, status_code=201,
    summary="Реєстрація користувача з існуючою локацією",
    description="Реєструє нового користувача та прив'язує його до вже існуючої локації. `location_id` має бути ID локації, яка вже є в базі даних. Якщо локація з таким ID не існує — буде повернута помилка.")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return schemas.UserRead.model_validate(db_user)

@router_user.put("/user/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    current_user: User = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    updated_user = crud.update_user(db, user_id, user)
    return schemas.UserRead.model_validate(updated_user)

@router_user.delete("/user/{user_id}", response_model=schemas.UserRead)
def delete_user(
    user_id: int,
    current_user: User = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")
    deleted_user = crud.delete_user(db, user_id)
    return schemas.UserRead.model_validate(deleted_user)

# ------------------- Login (OAuth2) -------------------

@router_login.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = services.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------- Advertisement -------------------

@router_ad.post("/advertisements/", response_model=schemas.AdvertisementRead, status_code=201)
def create_ad(
    ad: schemas.AdvertisementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(crud.get_current_user)
):
    ad.user_id = current_user.user_id
    return crud.create_advertisement(db, ad)

@router_ad.get("/advertisements/", response_model=list[schemas.AdvertisementRead])
def read_ads(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(crud.get_current_user)
):
    all_ads = crud.get_advertisements(db)
    visible_ads = []
    for ad in all_ads:
        if ad.public_status:
            visible_ads.append(ad)
        elif current_user and ad.location_id == current_user.location_id:
            visible_ads.append(ad)
    return visible_ads

@router_ad.get("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def read_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(crud.get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    if ad.public_status or (current_user and ad.location_id == current_user.location_id):
        return ad

    raise HTTPException(status_code=404, detail="Advertisement not found")

@router_ad.put("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def update_ad(
    ad_id: int,
    ad_data: schemas.AdvertisementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(crud.get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad or ad.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    updated = crud.update_advertisement(db, ad_id, ad_data)
    return updated

@router_ad.delete("/advertisements/{ad_id}", response_model=schemas.AdvertisementRead)
def delete_ad(
    ad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(crud.get_current_user)
):
    ad = crud.get_advertisement(db, ad_id)
    if not ad or ad.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Advertisement not found")

    deleted = crud.delete_advertisement(db, ad_id)
    return deleted
