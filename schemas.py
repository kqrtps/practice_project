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

class UserCreateWithLocation(BaseModel):
    username: str
    password: str
    location_name: str

class AdvertisementBase(BaseModel):
    title: str
    content: str
    public_status: bool = True

class AdvertisementCreate(AdvertisementBase):
    user_id: int
    location_id: int

class AdvertisementUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    public_status: bool | None = None
    location_id: int | None = None

class AdvertisementRead(AdvertisementBase):
    advertisement_id: int
    user_id: int
    location_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str