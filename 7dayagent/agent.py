import json
from datetime import datetime, timedelta
from google.adk.agents import LlmAgent
from google.genai import types

import logging
import os

# Using the specified model
MODEL_NAME = "openai/gpt-oss-20b"

# Step 3 - Configure API Key
# Retrieve the API key from the userdata dictionary and set it as an environment variable for use in API client initialization

OPENAI_API_BASE="http://localhost:1234/v1"
OPENAI_API_KEY="anything"
os.environ["OPENAI_API_BASE"] = OPENAI_API_BASE
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


# --- Weather Tool Implementation ---
def get_7day_weather_forecast(city: str) -> dict:
    """Simulates fetching 7-day weather forecast for a city"""
    print(f"\n-- Tool Call: get_7day_weather_forecast(city='{city}') --")

    # Mock data - in a real implementation you would call a weather API
    base_date = datetime.now()
    weather_conditions = ["Sunny", "Partly Cloudy", "Rainy", "Cloudy", "Thunderstorms"]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    forecast = []
    for day in range(7):
        current_date = base_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        day_of_week = days_of_week[current_date.weekday()]
        condition = weather_conditions[day % len(weather_conditions)]

        forecast.append({
            "date": date_str,
            "day_of_week": day_of_week,
            "high_temp": 20 + (day * 1.5),  # Varying temps for demo
            "low_temp": 10 + (day * 1.2),
            "conditions": condition,
            "precipitation_chance": 0.1 * (day % 3)  # Varying precip chance
        })

    result = {
        "city": city,
        "forecast": forecast,
        "units": "celsius"
    }

    print(f"-- Tool Result: {json.dumps(result, indent=2)} --")
    return result


# --- Helper Function for Agent Interaction ---
def get_weather_forecast(city: str):

    # ADK-specific: Configure logging to suppress GenAI warnings
    logging.getLogger("google_genai.types").setLevel(logging.ERROR)

    """Helper function to query the weather agent"""
    query = json.dumps({"city": city})
    print(f"\n>>> Getting weather for: {city}")

    user_content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response = None
    for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_content):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text

    if final_response:
        try:
            # Parse and pretty print the JSON response
            parsed = json.loads(final_response)
            print("<<< Weather Forecast:")
            print(json.dumps(parsed, indent=2))

            # Store in session for reference
            current_session = session_service.get_session(APP_NAME, USER_ID, SESSION_ID)
            current_session.state[weather_agent.output_key] = final_response
        except json.JSONDecodeError:
            print(f"<<< Received non-JSON response: {final_response}")
    else:
        print("<<< No response received")


# --- Configure the Weather Agent ---
from google.adk.models.lite_llm import LiteLlm
AGENT_MODEL = LiteLlm(
        model=MODEL_NAME,
        api_base=OPENAI_API_BASE,
        api_key=OPENAI_API_KEY
    )

root_agent = LlmAgent(
    model=AGENT_MODEL,
    name="weather_forecast_agent",
    description="Provides 7-day weather forecasts for cities worldwide",
    instruction="""You are a weather assistant that provides detailed 7-day forecasts.
The user will provide input in JSON format with city name.

1. Extract city from input
2. Use the get_7day_weather_forecast tool to fetch data
3. Return the forecast in user friendly format including the day of week

Example input: {"city": "New York"}

}""",
    tools=[get_7day_weather_forecast],
)

