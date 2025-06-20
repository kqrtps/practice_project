from sqlalchemy.orm import Session
from models import Location
from schemas import LocationCreate

def get_location(db: Session, location_id: int) -> Location | None:
    return db.query(Location).filter(Location.location_id == location_id).first()

def delete_location(db: Session, location_id: int) -> Location | None:
    db_location = db.query(Location).filter(Location.location_id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location