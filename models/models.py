from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str


class Property(BaseModel):
    property_name: str


class Floorplan(BaseModel):
    id: int
    name: str
    price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    square_feet: Optional[int] = None


class Property(BaseModel):
    property_name: str
    website: str


class InterestedFloorplan(BaseModel):
    user_id: int
    property_name: str
    floorplan_name: Optional[str] = None
