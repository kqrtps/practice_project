from pydantic import BaseModel
from typing import Optional

class LocationBase(BaseModel):
    location_name: str

class LocationCreate(LocationBase):
    pass

class LocationRead(LocationBase):
    location_id: int

    class Config:
        from_attributes = True

class LocationUpdate(LocationBase):
    pass



class UserBase(BaseModel):
    username:str

class UserRead(UserBase):
    user_id:int
    location_id:int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str
    location_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    location_id: Optional[int] = None

