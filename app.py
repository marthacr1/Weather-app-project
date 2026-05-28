import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
GEO_URL = "https://api.openweathermap.org/geo/1.0"


def get_coordinates(city: str):
    """Get lat/lon for a city name."""
    url = f"{GEO_URL}/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if not data:
        return None, None
    return data[0]["lat"], data[0]["lon"]


def get_current_weather(lat: float, lon: float):
    """Fetch current weather data."""
    url = f"{BASE_URL}/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_forecast(lat: float, lon: float):
    """Fetch 5-day / 3-hour forecast."""
    url = f"{BASE_URL}/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()


def parse_daily_forecast(forecast_data: dict) -> list:
    """Collapse 3-hour slots into daily summaries."""
    from collections import defaultdict

    days = defaultdict(list)
    for item in forecast_data.get("list", []):
        date = item["dt_txt"].split(" ")[0]
        days[date].append(item)

    daily = []
    for date, items in list(days.items())[:5]:
        temps = [i["main"]["temp"] for i in items]
        descriptions = [i["weather"][0]["description"] for i in items]
        icons = [i["weather"][0]["icon"] for i in items]
        daily.append(
            {
                "date": date,
                "temp_min": round(min(temps), 1),
                "temp_max": round(max(temps), 1),
                "description": max(set(descriptions), key=descriptions.count),
                "icon": max(set(icons), key=icons.count),
                "humidity": round(sum(i["main"]["humidity"] for i in items) / len(items)),
                "wind_speed": round(sum(i["wind"]["speed"] for i in items) / len(items), 1),
            }
        )
    return daily


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "City name is required."}), 400

    try:
        lat, lon = get_coordinates(city)
        if lat is None:
            return jsonify({"error": f"City '{city}' not found."}), 404

        current = get_current_weather(lat, lon)
        forecast_raw = get_forecast(lat, lon)
        daily = parse_daily_forecast(forecast_raw)

        return jsonify(
            {
                "city": current.get("name"),
                "country": current["sys"].get("country"),
                "current": {
                    "temp": round(current["main"]["temp"], 1),
                    "feels_like": round(current["main"]["feels_like"], 1),
                    "humidity": current["main"]["humidity"],
                    "description": current["weather"][0]["description"],
                    "icon": current["weather"][0]["icon"],
                    "wind_speed": current["wind"]["speed"],
                    "visibility": current.get("visibility", 0) // 1000,
                    "pressure": current["main"]["pressure"],
                },
                "forecast": daily,
            }
        )
    except requests.HTTPError as e:
        return jsonify({"error": f"API error: {e.response.status_code}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
