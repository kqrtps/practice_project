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