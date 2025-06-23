from pydantic import BaseModel

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
