from typing import List
from sqlmodel import select
from sqlalchemy import between
from app.core.database import SessionDep, db_session
from app.features.auth.models import Parking

def create_parking(parking: Parking) -> None:
    """Create a parking."""
    session: SessionDep = db_session.get()
    session.add(parking)
    session.commit()

def get_parking(id: int) -> Parking | None:
    """Get a parking by id."""
    session: SessionDep = db_session.get()
    statement = select(Parking).where(Parking.id == id)
    result = session.exec(statement).first()
    return result

def get_parkings_near(latitude: float, longitude: float, radius: float = 0.01) -> List[Parking]:
    """"Get parkings near a location."""
    session: SessionDep = db_session.get()
    statement = select(Parking).where(
        between(Parking.latitude, latitude - radius, latitude + radius) &
        between(Parking.longitude, longitude - radius, longitude + radius)
    )
    return list(session.exec(statement))