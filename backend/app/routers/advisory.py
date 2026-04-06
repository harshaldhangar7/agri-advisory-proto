from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/advisory", tags=["advisory"])

class Weather(BaseModel):
    rain_last_3_days: Optional[float] = 0.0

class AdvisoryRequest(BaseModel):
    plot_id: str
    symptoms: Optional[str] = None
    weather: Optional[Weather] = Weather()

@router.post("/recommend")
def recommend(req: AdvisoryRequest):
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
    return {"plot_id": req.plot_id, "advice": advice, "timestamp": __import__("datetime").datetime.utcnow().isoformat()}