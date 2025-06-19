from sqlalchemy.orm import Session
from models import Location

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Location).offset(skip).limit(limit).all()

def get_location(db: Session, location_id: int):
    return db.query(Location).filter(Location.location_id  == location_id).first()