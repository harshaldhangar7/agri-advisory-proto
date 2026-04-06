from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from ..models import Farmer, Plot
from ..db import get_engine

router = APIRouter(prefix="/api/farmers", tags=["farmers"])

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

@router.post("/", response_model=Farmer)
def create_farmer(f: Farmer, session: Session = Depends(get_session)):
    session.add(f)
    session.commit()
    session.refresh(f)
    return f

@router.post("/{farmer_id}/plots", response_model=Plot)
def add_plot(farmer_id: str, plot: Plot, session: Session = Depends(get_session)):
    farmer = session.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")
    plot.farmer_id = farmer_id
    session.add(plot)
    session.commit()
    session.refresh(plot)
    return plot

@router.get("/{farmer_id}")
def get_farmer(farmer_id: str, session: Session = Depends(get_session)):
    farmer = session.get(Farmer, farmer_id)
    if not farmer:
        raise HTTPException(status_code=404, detail="Not found")
    stmt = select(Plot).where(Plot.farmer_id == farmer_id)
    plots = session.exec(stmt).all()
    return {"farmer": farmer, "plots": plots}