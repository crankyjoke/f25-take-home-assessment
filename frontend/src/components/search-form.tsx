"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export function WeatherID() {
    const [inputId, setInputId] = useState("");
    const [weatherData, setWeatherData] = useState<any | null>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchWeather = async () => {
        try {
            const res = await fetch(`http://localhost:8000/weather/${inputId}`);
            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || "error");
            }

            const data = await res.json();
            setWeatherData(data);
            setError(null);
        } catch (err: any) {
            setError(err.message);
            setWeatherData(null);
        }
    };

    return (
        <Card className="w-full max-w-xl mt-6 mx-auto">
            <CardHeader>
                <CardTitle>Look Up Weather data by ID</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                <div className="flex gap-2">
                    <Input
                        type="text"
                        placeholder="Enter weather ID"
                        value={inputId}
                        onChange={(e) => setInputId(e.target.value)}
                    />
                    <Button onClick={fetchWeather}>Fetch</Button>
                </div>

                {error && <p className="text-red-500">{error}</p>}

                {weatherData && (
                    <div className="mt-4 space-y-2">
                        <p><strong>Date:</strong> {weatherData.date}</p>

                        <p><strong>Location:</strong> {weatherData.location}</p>


                        <p><strong>Notes:</strong> {weatherData.notes || "None"}</p>

                        {weatherData.weather?.current && (

                            <>
                                <p><strong>Temp:</strong> {weatherData.weather.current.temperature}  °C</p>
                                <p><strong>Condition:</strong> {weatherData.weather.current.weather_descriptions?.join(", ")}</p>
                                <img
                                    src={weatherData.weather.current.weather_icons?.[0]}
                                    alt="Weather Icon"
                                    className="h-12"
                                />
                            </>
                        )}
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
export default WeatherID;