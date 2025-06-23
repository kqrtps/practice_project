from sqlalchemy.orm import Session
from models import Location, User
from schemas import LocationCreate , LocationRead
from schemas import UserCreate, UserRead, UserUpdate

#Location

def create_location(db: Session, location: LocationCreate) -> Location:
    db_location = Location(location_name=location.location_name)
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

def create_user(db:Session, user:UserCreate)-> User:
    db_user = User(password=user.password, username=user.username,location_id=user.location_id)
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

def update_user(db:Session,user_id:int, user:UserUpdate)-> User | None:
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        return None
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = user.password
    if user.location_id is not None:
        db_user.location_id = user.location_id
    db.commit()
    db.refresh(db_user)
    return db_user






