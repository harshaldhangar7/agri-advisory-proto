from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import select, Session
from typing import List, Optional
import logging
from ..models import Farmer, Plot, FarmerCreate, FarmerUpdate, PlotCreate
from ..db import get_engine
from ..auth import get_current_user_id

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/farmers", tags=["farmers"])

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

@router.get("/", response_model=List[Farmer])
def list_farmers(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Get all farmers with pagination (requires authentication)"""
    try:
        stmt = select(Farmer).offset(skip).limit(limit)
        farmers = session.exec(stmt).all()
        logger.info(f"Retrieved {len(farmers)} farmers")
        return farmers
    except Exception as e:
        logger.error(f"Error listing farmers: {e}")
        raise HTTPException(status_code=500, detail="Error listing farmers")

@router.post("/", response_model=Farmer)
def create_farmer(
    farmer_data: FarmerCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Create a new farmer with validated input (requires authentication)"""
    try:
        # Create Farmer instance from validated FarmerCreate
        farmer = Farmer(**farmer_data.dict())
        session.add(farmer)
        session.commit()
        session.refresh(farmer)
        logger.info(f"Created farmer: {farmer.id}")
        return farmer
    except Exception as e:
        logger.error(f"Error creating farmer: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{farmer_id}", response_model=dict)
def get_farmer(
    farmer_id: str, 
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Get farmer details with plots (requires authentication)"""
    try:
        farmer = session.get(Farmer, farmer_id)
        if not farmer:
            logger.warning(f"Farmer not found: {farmer_id}")
            raise HTTPException(status_code=404, detail="Farmer not found")
        stmt = select(Plot).where(Plot.farmer_id == farmer_id)
        plots = session.exec(stmt).all()
        logger.info(f"Retrieved farmer {farmer_id} with {len(plots)} plots")
        return {"farmer": farmer, "plots": plots}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting farmer: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving farmer")

@router.put("/{farmer_id}", response_model=Farmer)
def update_farmer(
    farmer_id: str,
    updates: FarmerUpdate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Update farmer information with validated input (requires authentication)"""
    try:
        farmer = session.get(Farmer, farmer_id)
        if not farmer:
            logger.warning(f"Farmer not found for update: {farmer_id}")
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        # Update only provided fields with validated data
        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(farmer, field) and field != "id" and field != "plots":
                setattr(farmer, field, value)
        
        session.add(farmer)
        session.commit()
        session.refresh(farmer)
        logger.info(f"Updated farmer: {farmer_id}")
        return farmer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating farmer: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{farmer_id}")
def delete_farmer(
    farmer_id: str,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Delete a farmer (requires authentication)"""
    try:
        farmer = session.get(Farmer, farmer_id)
        if not farmer:
            logger.warning(f"Farmer not found for delete: {farmer_id}")
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        session.delete(farmer)
        session.commit()
        logger.info(f"Deleted farmer: {farmer_id}")
        return {"message": f"Farmer {farmer_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting farmer: {e}")
        raise HTTPException(status_code=500, detail="Error deleting farmer")

@router.post("/{farmer_id}/plots", response_model=Plot)
def add_plot(
    farmer_id: str, 
    plot_data: PlotCreate,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Add a plot to farmer with validated input (requires authentication)"""
    try:
        farmer = session.get(Farmer, farmer_id)
        if not farmer:
            logger.warning(f"Farmer not found: {farmer_id}")
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        # Create Plot instance from validated PlotCreate
        plot = Plot(**plot_data.dict(), farmer_id=farmer_id)
        session.add(plot)
        session.commit()
        session.refresh(plot)
        logger.info(f"Created plot {plot.id} for farmer {farmer_id}")
        return plot
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding plot: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{farmer_id}/plots", response_model=List[Plot])
def get_farmer_plots(
    farmer_id: str,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Get all plots for a farmer (requires authentication)"""
    try:
        farmer = session.get(Farmer, farmer_id)
        if not farmer:
            logger.warning(f"Farmer not found: {farmer_id}")
            raise HTTPException(status_code=404, detail="Farmer not found")
        
        stmt = select(Plot).where(Plot.farmer_id == farmer_id)
        plots = session.exec(stmt).all()
        logger.info(f"Retrieved {len(plots)} plots for farmer {farmer_id}")
        return plots
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plots: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving plots")

@router.delete("/{farmer_id}/plots/{plot_id}")
def delete_plot(
    farmer_id: str,
    plot_id: str,
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    """Delete a plot (requires authentication)"""
    try:
        plot = session.get(Plot, plot_id)
        if not plot or plot.farmer_id != farmer_id:
            logger.warning(f"Plot not found: {plot_id}")
            raise HTTPException(status_code=404, detail="Plot not found")
        
        session.delete(plot)
        session.commit()
        logger.info(f"Deleted plot {plot_id} from farmer {farmer_id}")
        return {"message": f"Plot {plot_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting plot: {e}")
        raise HTTPException(status_code=500, detail="Error deleting plot")