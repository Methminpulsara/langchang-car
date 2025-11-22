from typing import Optional, List
from pydantic import BaseModel, Field


class CarAnalysis(BaseModel):
    key_insights: str = Field(
        description="Important insights about the car deals across websites"
    )
    summary: str = Field(
        description="A short 2-3 sentence summary of the findings"
    )
    best_average_price: str = Field(
        description="Recommended best average price to buy this car model"
    )


class Car(BaseModel):
    id: str = Field(
        description="Unique ID for the scraped car listing"
    )
    title: str = Field(
        description="Title of the car advertisement"
    )
    make: str = Field(
        description="Car manufacturer brand (e.g., Toyota)"
    )
    model: str = Field(
        description="Car model (e.g., Axio, Premio)"
    )
    year: str = Field(
        description="Manufacturing year of the car"
    )
    mileage: str = Field(
        description="Mileage of the car, usually in kilometers"
    )
    price: str = Field(
        description="Listed price of the car in rupees"
    )
    location: Optional[str] = Field(
        default=None,
        description="Location of the seller or listing (optional)"
    )


class CarResponse(BaseModel):
    total_items: int = Field(
        description="Number of car listings extracted from all websites"
    )
    cars: List[Car] = Field(
        description="List of car listings with details"
    )
    analysis: CarAnalysis = Field(
        description="AI-powered analysis summarizing car deals"
    )
