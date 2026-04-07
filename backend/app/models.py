from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator, BaseModel
from uuid import uuid4

def gen_uuid():
    return str(uuid4())

# ============================================================================
# VALIDATION MODELS (for API requests - ensure data is valid before DB)
# ============================================================================

class FarmerValidation(BaseModel):
    """Validation model for farmer data"""
    name: str
    phone: Optional[str] = None
    language: Optional[str] = "mr"
    
    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        if len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v
    
    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        v = str(v).strip() if v else None
        if v and len(v) > 20:
            raise ValueError('Phone must be less than 20 characters')
        return v

class FarmerCreate(FarmerValidation):
    """Request model for creating farmers"""
    pass

class FarmerUpdate(BaseModel):
    """Request model for updating farmers - all fields optional"""
    name: Optional[str] = None
    phone: Optional[str] = None
    
    @field_validator('name', mode='before')
    @classmethod
    def validate_name(cls, v):
        if v is None:
            return None
        v = str(v).strip() if v else None
        if v and len(v) > 100:
            raise ValueError('Name must be less than 100 characters')
        return v
    
    @field_validator('phone', mode='before')
    @classmethod
    def validate_phone(cls, v):
        if v is None:
            return None
        v = str(v).strip() if v else None
        if v and len(v) > 20:
            raise ValueError('Phone must be less than 20 characters')
        return v

class PlotValidation(BaseModel):
    """Validation model for plot data"""
    name: str
    area_hectares: float
    crop: str
    
    @field_validator('name', mode='before')
    @classmethod
    def validate_plot_name(cls, v):
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError('Plot name cannot be empty')
        if len(v) > 100:
            raise ValueError('Plot name must be less than 100 characters')
        return v
    
    @field_validator('area_hectares')
    @classmethod
    def validate_area(cls, v):
        v = float(v)
        if v <= 0:
            raise ValueError('Area must be greater than 0')
        if v > 10000:
            raise ValueError('Area must be less than 10000 hectares')
        return v
    
    @field_validator('crop', mode='before')
    @classmethod
    def validate_crop(cls, v):
        if isinstance(v, str):
            v = v.strip()
        if not v:
            raise ValueError('Crop name cannot be empty')
        if len(v) > 50:
            raise ValueError('Crop name must be less than 50 characters')
        return v

class PlotCreate(PlotValidation):
    """Request model for creating plots"""
    pass

# ============================================================================
# DATABASE MODELS (for SQLModel table definitions)
# ============================================================================

class Farmer(SQLModel, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True, index=True)
    name: str
    phone: Optional[str] = None
    language: Optional[str] = "mr"
    plots: List["Plot"] = Relationship(back_populates="farmer")

class Plot(SQLModel, table=True):
    id: str = Field(default_factory=gen_uuid, primary_key=True, index=True)
    name: str
    area_hectares: float
    crop: str
    farmer_id: Optional[str] = Field(default=None, foreign_key="farmer.id")
    farmer: Optional[Farmer] = Relationship(back_populates="plots")