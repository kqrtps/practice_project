from sqlalchemy.orm import Session
from models import Location
from schemas import LocationCreate
from schemas import LocationRead
from models import Advertisement
from schemas import AdvertisementCreate, AdvertisementUpdate


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
    loc = db.query(Location).filter(location_id == Location.location_id).first()
    if loc is None:
        return None
    return LocationRead.model_validate(loc)


def delete_location(db: Session, location_id: int) -> Location | None:
    db_location = db.query(Location).filter(location_id == Location.location_id).first()
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

def create_advertisement(db: Session, ad: AdvertisementCreate) -> Advertisement:
    db_ad = Advertisement(**ad.dict())
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
    for field, value in ad_data.dict(exclude_unset=True).items():
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
