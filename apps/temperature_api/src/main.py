import random
from datetime import UTC, datetime
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

LOCATIONS = {"1": "Living Room", "2": "Bedroom", "3": "Kitchen"}


class TemperatureResponse(BaseModel):
    value: int = Field(ge=0, le=50)
    unit: str = "C"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    location: str
    status: str = "ok"
    sensor_id: str
    sensor_type: str = "DHT22"
    description: str = "Office temperature sensor"


app = FastAPI(title="Temperature API")


@app.get(path="/temperature")
async def get_temperature(location: Annotated[str, Query(description="Название локации")]) -> TemperatureResponse:
    if random.randint(1, 100) == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location Not Found Error")
    return TemperatureResponse(
        value=random.randint(0, 50),
        location=location,
        sensor_id=f"sensor-{random.randint(1, 100)}",
    )


@app.get(path="/temperature/{sensor_id}")
async def get_temperature_by_id(sensor_id: str) -> TemperatureResponse:
    return TemperatureResponse(
        value=random.randint(0, 50),
        location=LOCATIONS.get(sensor_id, "Unknown"),
        sensor_id=sensor_id,
    )


if __name__ == "__main__":
    uvicorn.run("src.main:app")
