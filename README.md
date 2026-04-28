# AI Activity Recommender — Powered by CrewAI

A multi-agent AI system that recommends the best activities for any location based on **live weather data**, **local events**, and **attraction research**. Four specialised agents collaborate sequentially, with a master concierge agent synthesising their findings into a full-day itinerary.

---

## Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│  Weather Analyst    │    │  Events Scout       │    │  Activities         │
│  (OpenWeatherMap)   │    │  (SerpAPI)          │    │  Researcher         │
│                     │    │                     │    │  (SerpAPI)          │
└────────┬────────────┘    └────────┬────────────┘    └────────┬────────────┘
         │                          │                          │
         └──────────────────────────┴──────────────────────────┘
                                    │  context
                         ┌──────────▼──────────┐
                         │  Master Concierge   │
                         │  (Recommendation)   │
                         └─────────────────────┘
```

| Agent | Role | Tool |
|---|---|---|
| **Weather Analyst** | Fetches live weather + 12h forecast | OpenWeatherMap API |
| **Events Scout** | Finds upcoming events & festivals | SerpAPI (Google Events) |
| **Activities Researcher** | Researches attractions & activities | SerpAPI (Google Search) |
| **Master Concierge** | Synthesises all data → full itinerary | (no external tool) |

---

## Quickstart (Conda + uv)

### 1. Clone & create the conda environment

```bash
git clone <repo-url>
cd ai-agents

# Create env with Python 3.11 only (no pip deps yet)
conda create -n ai-agents python=3.11 -c conda-forge -y
conda activate ai-agents
```

### 2. Install dependencies with uv

[`uv`](https://github.com/astral-sh/uv) is a fast Rust-based pip replacement (10–100× faster than plain pip).

```bash
pip install uv
uv pip install --python $(which python) -r requirements.txt
```

### 3. Set up environment variables

```bash
cp travel_agents/.env.example travel_agents/.env
# then edit travel_agents/.env with your API keys
```

You need three API keys:

| Key | Where to get it | Free tier |
|---|---|---|
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys | Pay-per-use |
| `SERPAPI_API_KEY` | https://serpapi.com/ | 250 searches/month |
| `OPENWEATHER_API_KEY` | https://openweathermap.org/api | 1,000 calls/day |

### 4. Run

```bash
cd travel_agents
python main.py
```

You will be prompted for a location, date, and any preferences.

---

## Project Structure

```
ai-agents/
├── environment.yml          # Conda environment definition
├── requirements.txt         # Pip dependencies
└── travel_agents/
    ├── main.py              # CLI entry point
    ├── crew.py              # Crew assembly & kickoff
    ├── agents.py            # Agent definitions
    ├── tasks.py             # Task definitions
    ├── tools.py             # Custom tools (weather + SerpAPI)
    └── .env.example         # Environment variable template
```

---

## Configuration

Edit `travel_agents/.env` to customise behaviour:

```dotenv
LLM_MODEL=gpt-4o            # swap to gpt-4-turbo, gpt-3.5-turbo, ollama/llama3, etc.
```

---

## Example Output

```
# Activity Recommendation Report

## 1. Weather Summary & Impact
Clear skies, 28°C — excellent outdoor conditions all day.

## 2. Must-Do Highlights
1. Petronas Twin Towers & KLCC Park
2. Batu Caves (morning visit before crowds)
3. Jalan Alor Night Market (evening street food)

## 3. Suggested Full-Day Itinerary
- Morning:   Batu Caves → sunrise hike, colourful temple steps
- Afternoon: KLCC Park & Aquaria KLCC
- Evening:   Jalan Alor street food tour

## 4. Special Events Today
- KL Jazz Festival @ Publika (8pm, ticketed)

## 5. Indoor Backup Plan
...
```
