from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_session
from app.features.parking.models import *
from app.features.parking.schemas import *
from app.features.parking.services import *

router = APIRouter(prefix="/parking", tags=["parking"], dependencies=[Depends(get_session)])

@router.post("/create")
async def create_parking(parking: ParkingCreateRequest) -> ParkingCreateResponse:
    """Create a new parking."""
    try:
        response: ParkingCreateResponse = create_parking_service(parking)
        return response
    except HTTPException as error:
        raise error
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Parking creation failed",
        ) from error
    
@router.get("/{parking_id}")
async def get_parking(parking_id: int) -> ParkingGetResponse:
    """Get parking by ID."""
    try:
        response: ParkingGetResponse = get_parking_service(parking_id)
        return response
    except HTTPException as error:
        raise error
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from error
    
@router.get("/")
def get_parkings_near(latitude: float, longitude: float, radius: int = 1000) -> ParkingNearResponse:
    """Get parkings near a location."""
    try:
        response: ParkingNearResponse = get_parkings_near_service(latitude, longitude, radius)
        return response
    except HTTPException as error:
        raise error
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from error