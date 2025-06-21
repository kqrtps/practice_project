
from sqlalchemy.orm import Session
from models import Location
from schemas import LocationCreate
from schemas import LocationRead

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