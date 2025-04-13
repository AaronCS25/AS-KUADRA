from fastapi import HTTPException, status
from .models import *
from .schemas import *
from .repositories import (create_parking as repository_create_parking)
from .repositories import (get_parking as repository_get_parking)
from .repositories import (get_parkings_near as repository_get_parkings_near)

def create_parking_service(parking_schema: ParkingCreateRequest) -> ParkingCreateResponse:
    """Create a new parking."""
    parking: Parking = Parking(**parking_schema.model_dump())
    repository_create_parking(parking)
    
    if not parking.id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Parking creation failed",
        )
    
    return ParkingCreateResponse(
        id=parking.id if parking.id is not None else 0,
        title=parking.title,
        address=parking.address,
        latitude=parking.latitude,
        longitude=parking.longitude,
        capacity=parking.capacity,
        available_spots=parking.available_spots,
        owner_id=parking.owner_id,
    )

def get_parking_service(parking_id: int) -> ParkingGetResponse:
    """Get parking by ID."""
    parking: Parking | None = repository_get_parking(parking_id)
    
    if not parking or parking.id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking not found",
        )
    
    return ParkingGetResponse(
        id=parking.id,
        title=parking.title,
        address=parking.address,
        latitude=parking.latitude,
        longitude=parking.longitude,
        capacity=parking.capacity,
        available_spots=parking.available_spots,
        owner_id=parking.owner_id,
    )

def get_parkings_near_service(latitude: float, longitude: float, radius: int) -> ParkingNearResponse:
    """Get parkings near a location."""
    parkings: list[Parking] = repository_get_parkings_near(latitude, longitude, radius)

    
    if not parkings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No parkings found in the specified area",
        )
    
    return ParkingNearResponse(
        parkings=[
            ParkingGetResponse(
                id=parking.id if parking.id is not None else 0,
                title=parking.title,
                address=parking.address,
                latitude=parking.latitude,
                longitude=parking.longitude,
                capacity=parking.capacity,
                available_spots=parking.available_spots,
                owner_id=parking.owner_id,
            ) for parking in parkings
        ]
    )