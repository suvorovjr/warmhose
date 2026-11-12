import random
import uvicorn
from datetime import UTC, datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field


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


if __name__ == "__main__":
    uvicorn.run("src.main:app")
