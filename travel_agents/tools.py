import os
import json
import requests
from crewai.tools import tool


@tool("Get Current Weather and Forecast")
def get_weather(location: str) -> str:
    """
    Fetches the current weather conditions and a short forecast for a given location.
    Input should be a city name, optionally with country code (e.g. 'London, UK').
    Returns temperature, humidity, wind, weather description and outdoor suitability.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY is not set in environment variables."

    try:
        current_url = "https://api.openweathermap.org/data/2.5/weather"
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"q": location, "appid": api_key, "units": "metric"}

        current_resp = requests.get(current_url, params=params, timeout=10)
        current_resp.raise_for_status()
        current = current_resp.json()

        forecast_resp = requests.get(forecast_url, params=params, timeout=10)
        forecast_resp.raise_for_status()
        forecast = forecast_resp.json()

        temp = current["main"]["temp"]
        feels_like = current["main"]["feels_like"]
        humidity = current["main"]["humidity"]
        description = current["weather"][0]["description"].title()
        wind_speed = current["wind"]["speed"]
        visibility = current.get("visibility", "N/A")
        city_name = current.get("name", location)
        country = current.get("sys", {}).get("country", "")

        outdoor_suitable = (
            description not in ["Heavy Rain", "Thunderstorm", "Snow", "Blizzard"]
            and temp > 10
            and wind_speed < 15
        )

        next_slots = forecast["list"][:4]
        forecast_summary = []
        for slot in next_slots:
            forecast_summary.append(
                f"  {slot['dt_txt']}: {slot['weather'][0]['description'].title()}, "
                f"{slot['main']['temp']:.1f}°C"
            )

        result = {
            "location": f"{city_name}, {country}",
            "current_conditions": {
                "temperature_celsius": round(temp, 1),
                "feels_like_celsius": round(feels_like, 1),
                "humidity_percent": humidity,
                "description": description,
                "wind_speed_ms": wind_speed,
                "visibility_meters": visibility,
            },
            "outdoor_activity_suitable": outdoor_suitable,
            "next_12h_forecast": forecast_summary,
        }
        return json.dumps(result, indent=2)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Error: Location '{location}' not found. Try a more specific city name."
        return f"Error fetching weather: {str(e)}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


@tool("Search Local Events")
def search_events(query: str) -> str:
    """
    Searches for upcoming local events, festivals, concerts, sports events, and community
    gatherings in a specific location using SerpAPI.
    Input should be a search query like 'events in Kuala Lumpur this weekend'.
    Returns a list of events with title, date, address, and description.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set in environment variables."

    try:
        from serpapi import GoogleSearch

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 10,
            "gl": "us",
            "hl": "en",
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        output_lines = []

        events = results.get("events_results", [])
        if events:
            output_lines.append("=== UPCOMING EVENTS ===")
            for event in events[:8]:
                when = event.get("date", {}).get("when", "Date TBD")
                address = ", ".join(event.get("address", ["Location TBD"]))
                output_lines.append(
                    f"- {event.get('title', 'Unknown Event')}\n"
                    f"  Date: {when}\n"
                    f"  Location: {address}\n"
                    f"  Info: {event.get('description', 'No description available')}"
                )

        organic = results.get("organic_results", [])
        if organic:
            output_lines.append("\n=== WEB RESULTS ===")
            for r in organic[:5]:
                output_lines.append(
                    f"- {r.get('title', '')}\n"
                    f"  {r.get('snippet', '')}\n"
                    f"  Link: {r.get('link', '')}"
                )

        return "\n".join(output_lines) if output_lines else "No events found for this query."

    except ImportError:
        return "Error: 'google-search-results' package is not installed. Run: pip install google-search-results"
    except Exception as e:
        return f"Error searching events: {str(e)}"


@tool("Search Local Activities and Attractions")
def search_activities(query: str) -> str:
    """
    Searches for popular local activities, tourist attractions, restaurants, parks, museums,
    and things to do in a specific location using SerpAPI.
    Input should be a search query like 'best things to do in Tokyo' or 'indoor activities Bangkok'.
    Returns places with name, rating, type, and address.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY is not set in environment variables."

    try:
        from serpapi import GoogleSearch

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "num": 10,
            "gl": "us",
            "hl": "en",
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        output_lines = []

        local_places = results.get("local_results", {}).get("places", [])
        if local_places:
            output_lines.append("=== LOCAL PLACES & ATTRACTIONS ===")
            for place in local_places[:8]:
                rating = place.get("rating", "N/A")
                reviews = place.get("reviews", "")
                reviews_str = f" ({reviews} reviews)" if reviews else ""
                output_lines.append(
                    f"- {place.get('title', 'Unknown')}\n"
                    f"  Type: {place.get('type', 'N/A')}\n"
                    f"  Rating: {rating}{reviews_str}\n"
                    f"  Address: {place.get('address', 'N/A')}\n"
                    f"  Hours: {place.get('hours', 'N/A')}"
                )

        organic = results.get("organic_results", [])
        if organic:
            output_lines.append("\n=== TOP RECOMMENDATIONS FROM WEB ===")
            for r in organic[:5]:
                output_lines.append(
                    f"- {r.get('title', '')}\n"
                    f"  {r.get('snippet', '')}"
                )

        return "\n".join(output_lines) if output_lines else "No activities found for this query."

    except ImportError:
        return "Error: 'google-search-results' package is not installed. Run: pip install google-search-results"
    except Exception as e:
        return f"Error searching activities: {str(e)}"
