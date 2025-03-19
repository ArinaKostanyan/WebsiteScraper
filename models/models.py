from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    name: str


class InterestedFloorplan(BaseModel):
    user_id: int
    property_name: str
    floorplan_name: Optional[str] = None
