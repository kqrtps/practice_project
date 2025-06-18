from sqlalchemy import Column, Integer, String ,ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(String, primary_key=True)
    location_name=Column(String)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    location_id=Column(String, ForeignKey('locations.location_id'))

