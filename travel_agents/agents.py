import os
from crewai import Agent, LLM
from tools import get_weather, search_events, search_activities


def _get_llm() -> LLM:
    model = os.getenv("LLM_MODEL", "gpt-4o")
    return LLM(model=model, temperature=0.7)


def create_weather_agent() -> Agent:
    return Agent(
        role="Meteorologist & Weather Analyst",
        goal=(
            "Retrieve accurate, up-to-date weather data for the target location and provide "
            "a clear assessment of whether conditions are suitable for outdoor or indoor activities."
        ),
        backstory=(
            "You are a seasoned meteorologist with 20 years of experience interpreting weather "
            "patterns. You translate raw weather data into practical, actionable insights that "
            "help people make smart decisions about their day. You always flag rain, extreme heat, "
            "strong winds, or any hazardous conditions that would affect activity planning."
        ),
        tools=[get_weather],
        llm=_get_llm(),
        max_iter=1,
        verbose=True,
        allow_delegation=False,
    )


def create_events_agent() -> Agent:
    return Agent(
        role="Local Events Scout",
        goal=(
            "Discover and report on upcoming events, festivals, concerts, sports matches, "
            "exhibitions, and community gatherings happening in the target location."
        ),
        backstory=(
            "You are an enthusiastic local culture correspondent who knows everything that's "
            "happening around town. You have a talent for finding both mainstream events and "
            "hidden local gems — from rooftop concerts and food festivals to pop-up markets and "
            "night bazaars. You always prioritise time-sensitive and unique experiences that "
            "visitors shouldn't miss."
        ),
        tools=[search_events],
        llm=_get_llm(),
        max_iter=2,
        verbose=True,
        allow_delegation=False,
    )


def create_activities_agent() -> Agent:
    return Agent(
        role="Activities & Attractions Researcher",
        goal=(
            "Research and compile the best activities, tourist attractions, dining spots, "
            "entertainment venues, and hidden local experiences available in the target location."
        ),
        backstory=(
            "You are a well-travelled writer and local guide who has explored hundreds of cities. "
            "You cover every category: outdoor adventures, cultural experiences, family-friendly "
            "spots, romantic settings, budget-friendly gems, and luxurious treats. You always "
            "note practical details like indoor vs outdoor, accessibility, and typical cost range "
            "so the recommendation master can filter options based on weather and preferences."
        ),
        tools=[search_activities],
        llm=_get_llm(),
        max_iter=2,
        verbose=True,
        allow_delegation=False,
    )


def create_master_agent() -> Agent:
    return Agent(
        role="Chief Activity Recommendation Concierge",
        goal=(
            "Synthesise the weather report, local event listings, and activity research to "
            "produce the perfect, tailored activity itinerary for the visitor — one that is "
            "weather-appropriate, highlights unmissable time-sensitive events, and balances "
            "variety across morning, afternoon, and evening."
        ),
        backstory=(
            "You are a world-class travel concierge with expertise in curating bespoke daily "
            "experiences. You think holistically: you cross-reference the weather conditions, "
            "event schedules, and the full range of available activities to craft recommendations "
            "that are practical, memorable, and safe. When rain threatens, you pivot to equally "
            "compelling indoor alternatives without missing a beat. Your recommendations are "
            "always specific, structured, and actionable — never vague or generic."
        ),
        tools=[],
        llm=_get_llm(),
        verbose=True,
        allow_delegation=True,
    )
