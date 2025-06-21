import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn
import requests


app = FastAPI(title="Weather Data System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for weather data


weather_storage: Dict[str, Dict[str, Any]] = {}

API_KEY = "2218a5827ddf836ee9f341a67e53c536"


class WeatherRequest(BaseModel):
    date: str
    location: str
    notes: Optional[str] = ""

class WeatherResponse(BaseModel):
    id: str

@app.post("/weather", response_model=WeatherResponse)
async def create_weather_request(request: WeatherRequest):
    """
    You need to implement this endpoint to handle the following:
    1. Receive form data (date, location, notes)
    2. Calls WeatherStack API for the location
    3. Stores combined data with unique ID in memory
    4. Returns the ID to frontend
    """
    # if request.date == "current":
    response = requests.get(
        "http://api.weatherstack.com/current",
        params={"access_key": API_KEY, "query": request.location}
    )
    # else:
    #     response = requests.get(
    #         "http://api.weatherstack.com/historical",
    #         params={
    #             "access_key": API_KEY,
    #             "query": request.location,
    #             "historical_date": request.date,
    #             "hourly": 1
    #         }
    #     )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Weather API error")

    data = response.json()
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"].get("info", "Unknown error"))
    weather_id = str(uuid.uuid4())
    weather_storage[weather_id] = {
        "date": request.date,
        "location": request.location,
      "notes": request.notes,
        "weather": data
    }
    # print(weather_storage)

    return WeatherResponse(id=weather_id)

@app.get("/weather/{weather_id}")
async def get_weather_data(weather_id: str):
    """
    Retrieve stored weather data by ID.
    This endpoint is already implemented for the assessment.
    """
    if weather_id not in weather_storage:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    return weather_storage[weather_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)