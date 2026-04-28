from crewai import Crew, Process
from tasks import build_crew_tasks


def run_activity_crew(location: str, date: str, preferences: str = "") -> str:
    """
    Assembles the four-agent crew and kicks off a sequential run.

    Args:
        location    : City / region for the activity search (e.g. 'Kuala Lumpur, Malaysia')
        date        : Day of interest (e.g. 'today', 'tomorrow', '2025-05-10')
        preferences : Optional visitor preferences (e.g. 'family with kids, budget-friendly')

    Returns:
        The final recommendation report as a string.
    """
    tasks, agents = build_crew_tasks(location, date, preferences)

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return str(result)
