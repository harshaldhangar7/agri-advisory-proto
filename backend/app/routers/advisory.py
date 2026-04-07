from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import logging
from ..models import Plot
from ..db import get_engine
from ..utils import verify_api_key

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/advisory", tags=["advisory"])

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

class Weather(BaseModel):
    rain_last_3_days: Optional[float] = 0.0
    
    @field_validator('rain_last_3_days')
    @classmethod
    def validate_rain(cls, v):
        if v < 0:
            raise ValueError('Rain cannot be negative')
        if v > 500:
            raise ValueError('Rain value must be less than 500mm')
        return v

class AdvisoryRequest(BaseModel):
    plot_id: str
    symptoms: Optional[str] = None
    weather: Optional[Weather] = Weather()
    
    @field_validator('symptoms')
    @classmethod
    def validate_symptoms(cls, v):
        if v and len(v) > 500:
            raise ValueError('Symptoms description must be less than 500 characters')
        return v.strip() if v else None

@router.post("/recommend")
def recommend(
    req: AdvisoryRequest, 
    session: Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    """Get agricultural advisory for a plot"""
    try:
        # Validate that plot exists
        plot = session.get(Plot, req.plot_id)
        if not plot:
            logger.warning(f"Plot not found for advisory: {req.plot_id}")
            raise HTTPException(status_code=404, detail=f"Plot {req.plot_id} not found")
        
        advice = []
        s = (req.symptoms or "").lower()
        if "yellow" in s or "yellowing" in s:
            advice.append("Possible nitrogen deficiency. Recommend soil test and apply NPK as per test.")
        if "spots" in s or "blight" in s:
            advice.append("Possible fungal infection. Use recommended fungicide and remove affected leaves.")
        if req.weather and req.weather.rain_last_3_days and req.weather.rain_last_3_days > 20:
            advice.append("High moisture detected. Avoid waterlogging and check drainage.")
        if not advice:
            advice.append("No specific issues detected. Continue regular monitoring and report changes.")
        
        logger.info(f"Generated advisory for plot {req.plot_id}")
        return {"plot_id": req.plot_id, "advice": advice, "timestamp": datetime.utcnow().isoformat()}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating advisory: {e}")
        raise HTTPException(status_code=500, detail="Error generating advisory")