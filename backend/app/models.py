from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4

def gen_uuid():
    return str(uuid4())

class FarmerBase(SQLModel):
    name: str
    phone: Optional[str] = None
    language: Optional[str] = "mr"

class Farmer(FarmerBase, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True, index=True)
    plots: List["Plot"] = Relationship(back_populates="farmer")

class PlotBase(SQLModel):
    name: str
    area_hectares: float
    crop: str

class Plot(PlotBase, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True, index=True)
    farmer_id: Optional[str] = Field(default=None, foreign_key="farmer.id")
    farmer: Optional[Farmer] = Relationship(back_populates="plots")