import os
import sys
from dotenv import load_dotenv

load_dotenv()


REQUIRED_ENV_VARS = {
    "OPENAI_API_KEY": "OpenAI API key (for the LLM powering all agents)",
    "SERPAPI_API_KEY": "SerpAPI key (https://serpapi.com/) for event & activity search",
    "OPENWEATHER_API_KEY": "OpenWeatherMap API key (https://openweathermap.org/api) for weather data",
}


def _check_env() -> bool:
    missing = []
    for var, description in REQUIRED_ENV_VARS.items():
        if not os.getenv(var):
            missing.append(f"  • {var}  —  {description}")
    if missing:
        print("\n❌  Missing required environment variables:")
        for m in missing:
            print(m)
        print(
            "\nCreate a .env file in the travel_agents/ directory based on .env.example "
            "and fill in the values above.\n"
        )
        return False
    return True


def _prompt(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value if value else default


def main() -> None:
    print("\n" + "=" * 60)
    print("  🌍  AI Activity Recommender  —  Powered by CrewAI")
    print("=" * 60)

    if not _check_env():
        sys.exit(1)

    print("\nEnter trip details (press Enter to use the default):\n")
    location = _prompt("📍 Location (city, country)", "Kuala Lumpur, Malaysia")
    date = _prompt("📅 Date (today / tomorrow / YYYY-MM-DD)", "today")
    preferences = _prompt(
        "🎯 Preferences or constraints (optional, e.g. 'family with kids, free activities')",
        "",
    )

    print(
        f"\n🤖  Launching 4 AI agents for {location} on {date}...\n"
        "   (This may take a minute — agents are working in sequence)\n"
        + "-" * 60
    )

    from crew import run_activity_crew

    result = run_activity_crew(location, date, preferences)

    print("\n" + "=" * 60)
    print("  📋  FINAL ACTIVITY RECOMMENDATIONS")
    print("=" * 60 + "\n")
    print(result)
    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
