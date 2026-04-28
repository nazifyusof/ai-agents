from crewai import Task
from agents import (
    create_weather_agent,
    create_events_agent,
    create_activities_agent,
    create_master_agent,
)


def build_crew_tasks(location: str, date: str, preferences: str = ""):
    """
    Instantiate agents and construct the four sequential CrewAI tasks.

    Returns:
        tasks   (list[Task])  — ordered task list for the Crew
        agents  (dict)        — keyed agent instances
    """
    weather_agent = create_weather_agent()
    events_agent = create_events_agent()
    activities_agent = create_activities_agent()
    master_agent = create_master_agent()

    pref_note = f"\nVisitor preferences / constraints: {preferences}" if preferences else ""

    weather_task = Task(
        description=(
            f"Fetch the current weather conditions and short-range forecast for **{location}** "
            f"on **{date}**.\n\n"
            "Use the 'Get Current Weather and Forecast' tool with the location as input.\n\n"
            "Your analysis must cover:\n"
            "- Current temperature (°C) and feels-like temperature\n"
            "- Sky conditions (clear, cloudy, rainy, stormy, etc.)\n"
            "- Humidity percentage and wind speed\n"
            "- Visibility conditions\n"
            "- 12-hour outlook\n"
            "- A clear verdict: are conditions SUITABLE or NOT SUITABLE for outdoor activities "
            "and why?\n"
            f"{pref_note}"
        ),
        expected_output=(
            "A structured weather brief containing:\n"
            "1. Current conditions summary (temp, humidity, wind, sky)\n"
            "2. 12-hour forecast highlights\n"
            "3. Outdoor activity suitability verdict with reasoning\n"
            "4. Any weather warnings or comfort flags (e.g. heat index, UV, heavy rain)"
        ),
        agent=weather_agent,
    )

    events_task = Task(
        description=(
            f"Search for upcoming events and special happenings in **{location}** around **{date}**.\n\n"
            "Use the 'Search Local Events' tool with queries such as:\n"
            f"  - 'events in {location} {date}'\n"
            f"  - 'festivals concerts {location} this week'\n"
            f"  - 'things happening {location} {date}'\n\n"
            "Focus on:\n"
            "- Local festivals and cultural celebrations\n"
            "- Concerts, live music, and performances\n"
            "- Sports events and competitions\n"
            "- Food & drink events (markets, pop-ups)\n"
            "- Exhibitions and art shows\n"
            "- Family-friendly community events\n"
            f"{pref_note}"
        ),
        expected_output=(
            "A curated list of 5–10 events in the area, each with:\n"
            "- Event name\n"
            "- Date and time\n"
            "- Venue / address\n"
            "- Brief description of the event\n"
            "- Estimated cost (free / paid) if available"
        ),
        agent=events_agent,
    )

    activities_task = Task(
        description=(
            f"Research and compile the best activities and attractions in **{location}**.\n\n"
            "Use the 'Search Local Activities and Attractions' tool with queries such as:\n"
            f"  - 'best things to do in {location}'\n"
            f"  - 'top outdoor activities {location}'\n"
            f"  - 'indoor attractions {location}'\n"
            f"  - 'best restaurants and food experiences {location}'\n\n"
            "Cover at least these categories:\n"
            "- Outdoor (parks, nature, adventure, beaches, hiking)\n"
            "- Cultural (museums, galleries, heritage sites, temples)\n"
            "- Entertainment (shopping, night life, cinemas)\n"
            "- Food & dining (local street food, signature dishes, cafes)\n"
            "- Relaxation (spas, gardens, scenic viewpoints)\n"
            f"{pref_note}"
        ),
        expected_output=(
            "A categorised list of 10–15 activities/attractions, each with:\n"
            "- Name and brief description\n"
            "- Category (outdoor / indoor / dining / entertainment)\n"
            "- Rating and typical visitor sentiment\n"
            "- Approximate cost range\n"
            "- Best time of day to visit"
        ),
        agent=activities_agent,
    )

    recommendation_task = Task(
        description=(
            f"You are the Chief Concierge. Using the weather report, the events list, and the "
            f"activities research provided by your colleagues, craft the **ultimate activity "
            f"guide** for a visitor to **{location}** on **{date}**.\n\n"
            "Your job is to:\n"
            "1. Select the BEST activity for each time slot based on weather suitability.\n"
            "2. Prioritise any time-sensitive or unique events that shouldn't be missed.\n"
            "3. Ensure a balanced, enjoyable day with variety.\n"
            "4. Provide indoor backup options for every outdoor suggestion.\n"
            "5. Add practical tips (transport, dress code, booking needed, etc.).\n"
            f"{pref_note}\n\n"
            "Structure your final output clearly with sections as described below."
        ),
        expected_output=(
            "# Activity Recommendation Report\n\n"
            "## 1. Weather Summary & Impact\n"
            "Brief weather snapshot and how it shapes today's plan.\n\n"
            "## 2. Must-Do Highlights\n"
            "Top 3 experiences not to miss today (with rationale).\n\n"
            "## 3. Suggested Full-Day Itinerary\n"
            "- **Morning (8am–12pm):** [activity, location, tips]\n"
            "- **Afternoon (12pm–6pm):** [activity + lunch recommendation]\n"
            "- **Evening (6pm onwards):** [activity/dining + any evening events]\n\n"
            "## 4. Special Events Today\n"
            "Any events happening today worth attending.\n\n"
            "## 5. Indoor Backup Plan\n"
            "Full alternative itinerary if weather deteriorates.\n\n"
            "## 6. Practical Tips\n"
            "Transport, dress code, booking advice, safety notes."
        ),
        agent=master_agent,
        context=[weather_task, events_task, activities_task],
    )

    tasks = [weather_task, events_task, activities_task, recommendation_task]
    agents = {
        "weather": weather_agent,
        "events": events_agent,
        "activities": activities_agent,
        "master": master_agent,
    }
    return tasks, agents
