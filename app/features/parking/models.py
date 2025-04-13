from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.features.auth.models import User

class Parking(SQLModel, table=True):
    __tablename__ = "parkings"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    address: str = Field(index=True, nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    capacity: int   = Field(nullable=False)
    available_spots: int = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

    owner_id: int = Field(foreign_key="users.id", nullable=False)
    owner: "User" = Relationship(back_populates="parkings")
