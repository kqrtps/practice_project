
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from database import Base



class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    location_name=Column(String)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)
    location_id=Column(Integer, ForeignKey('locations.location_id'))

class Advertisement(Base):
    __tablename__ = 'advertisement'
    advertisement_id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    public_status = Column(Boolean)  # True - публічне, False - локальне
    user_id = Column(Integer, ForeignKey('users.user_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
