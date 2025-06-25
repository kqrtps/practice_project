from sqlalchemy.orm import Session
from database import get_db
from models import Location, User
from schemas import LocationCreate , LocationRead
from schemas import UserCreate, UserRead, UserUpdate
from models import Advertisement
from schemas import AdvertisementCreate, AdvertisementUpdate
from services import hash_password, verify_password, SECRET_KEY, ALGORITHM
from jose import jwt , JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


#Location
def get_location_by_name(db: Session, name: str) -> Location | None:
    return db.query(Location).filter(Location.location_name == name).first()

def create_location(db: Session, location: LocationCreate, current_user_id: int) -> Location:
    loc  = get_location_by_name(db, location.location_name)
    if  loc:
        raise HTTPException(status_code=400, detail="Location with this name already exists")

    db_location = Location(location_name=location.location_name, owner_id=current_user_id)
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


#def get_locations(db: Session) -> list[Location]:
    #return db.query(Location).all()

def get_locations(db: Session) -> list[LocationRead]:
    return [LocationRead.model_validate(loc) for loc in db.query(Location).all()]

#def get_location(db: Session, location_id: int) -> Location | None:
    #return db.query(Location).filter(Location.location_id == location_id).first()

def get_location(db: Session, location_id: int) -> LocationRead | None:
    loc = db.query(Location).filter(Location.location_id == location_id).first()
    if loc is None:
        return None
    return LocationRead.model_validate(loc)

def delete_location(db: Session, location_id: int) -> Location | None:
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location

def update_location(db: Session, location_id: int, new_name: str) -> Location | None:
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location is None:
        return None
    db_location.location_name = new_name
    db.commit()
    db.refresh(db_location)
    return db_location


#User
def create_user_with_location(db: Session, username: str, password: str, location_name: str) -> User:
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.flush()  # отримаємо user_id, але ще не комітимо

    new_location = Location(location_name=location_name, owner_id=new_user.user_id)
    db.add(new_location)
    db.flush()

    new_user.location_id = new_location.location_id  # якщо модель має таке поле

    db.commit()
    db.refresh(new_user)
    return new_user

def create_user(db:Session, user:UserCreate)-> User:
    location = db.query(Location).filter(Location.location_id == user.location_id).first()
    if location is None:
        raise HTTPException(status_code=400, detail="Location with this ID does not exist")
    hashed_password = hash_password(user.password)
    db_user = User(password=hashed_password, username=user.username,location_id=user.location_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session, user_id:int)-> UserRead | None :
    us = db.query(User).filter(User.user_id == user_id).first()
    if us is None:
        return None
    return UserRead.model_validate(us)

def delete_user(db:Session, user_id:int)->User | None:
    db_user= db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> User | None:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        return None

    updated = False

    if user.username is not None and user.username != db_user.username:
        existing = db.query(User).filter(User.username == user.username).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")
        db_user.username = user.username
        updated = True

    if user.password is not None:
        db_user.password = hash_password(user.password)
        updated = True

    if user.location_id is not None:
        location = db.query(Location).filter(Location.location_id == user.location_id).first()
        if not location:
            raise HTTPException(status_code=400, detail="Location with this ID does not exist")
        db_user.location_id = user.location_id
        updated = True

    if updated:
        db.commit()
        db.refresh(db_user)

    return db_user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

# Advertisiment
def create_advertisement(db: Session, ad: AdvertisementCreate) -> Advertisement:
    db_ad = Advertisement(**ad.model_dump())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def get_advertisement(db: Session, ad_id: int) -> Advertisement | None:
    return db.query(Advertisement).filter(Advertisement.advertisement_id == ad_id).first()

def get_advertisements(db: Session) -> list[Advertisement]:
    return db.query(Advertisement).all()

def update_advertisement(db: Session, ad_id: int, ad_data: AdvertisementUpdate) -> Advertisement | None:
    db_ad = db.query(Advertisement).filter(Advertisement.advertisement_id == ad_id).first()
    if not db_ad:
        return None
    for field, value in ad_data.model_dump(exclude_unset=True).items():
        setattr(db_ad, field, value)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def delete_advertisement(db: Session, ad_id: int) -> Advertisement | None:
    db_ad = db.query(Advertisement).filter(Advertisement.advertisement_id == ad_id).first()
    if db_ad:
        db.delete(db_ad)
        db.commit()
    return db_ad

