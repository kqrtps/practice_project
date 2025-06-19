from pydantic import BaseModel

class LocationRead(BaseModel):
    location_id: int
    location_name: str

    class Config:
        orm_mode = True  # дозволяє працювати з ORM-об'єктами поясни все порядково і для чого це