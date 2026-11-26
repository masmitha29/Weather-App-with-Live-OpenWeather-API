
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# Function to call the weather API
def get_weather(url, city):

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url, params=params, timeout=10
        )

        if response.status_code == 404:
            print("Error: City not found!")
            return None

        if response.status_code == 401:
            print("Error: Invalid API key!")
            return None

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:
        print("Network/API error:", error)
        return None


# Display current weather
def display_weather(city):

    data = get_weather(BASE_URL, city)

    if data is None:
        return

    main = data.get("main", {})
    weather = data.get("weather", [{}])
    wind = data.get("wind", {})

    print("\n========== CURRENT WEATHER ==========")

    print("City:", data.get("name", city))
    print("Temperature:", main.get("temp", "N/A"), "°C")
    print("Humidity:", main.get("humidity", "N/A"), "%")

    description = weather[0].get("description", "N/A") if weather else "N/A"

    print("Weather:", description)
    print("Wind Speed:", wind.get("speed", "N/A"), "m/s")


# Display five-day forecast
def display_forecast(city):

    data = get_weather(FORECAST_URL, city)

    if data is None:
        return

    daily_forecast = {}

    for item in data.get("list", []):

        date = item.get("dt_txt", "")[:10]
        time = item.get("dt_txt", "")[11:16]

        if date and date not in daily_forecast:

            daily_forecast[date] = item

        # Prefer the midday forecast for each day
        if date and time == "12:00":

            daily_forecast[date] = item

    print("\n========== FIVE DAY FORECAST ==========")

    print(f"{'DATE':<15} {'TEMP':<12} {'CONDITION'}")
    print("-" * 50)

    for date, item in daily_forecast.items():

        temperature = item.get("main", {}).get("temp", "N/A")

        weather = item.get("weather", [{}])
        description = (
            weather[0].get("description", "N/A")
            if weather else "N/A"
        )

        print(f"{date:<15} {str(temperature) + ' C':<12} {description}")

    print("-" * 50)


# Main program
print("=" * 45)
print("       PYTHON WEATHER APPLICATION")
print("=" * 45)

if not API_KEY:
    print("API key missing! Please check your .env file.")

else:

    while True:

        city = input("\nEnter city name (or press Enter to exit): ").strip()

        if city == "":
            print("Thank you for using Weather App!")
            break

        display_weather(city)
        display_forecast(city)
