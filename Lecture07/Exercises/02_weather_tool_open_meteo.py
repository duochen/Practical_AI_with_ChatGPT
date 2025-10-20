
# Lesson 7 – Exercise 2
# Title: Weather Tool via Open‑Meteo (no API key required)
#
# GOAL
# - Connect ChatGPT to a real external API and return structured JSON.
# - Use the Function Calling (tools) pattern end-to-end.
#
# WHAT IT DOES
# - Defines a tool get_weather(lat, lon) that calls Open-Meteo's forecast API.
# - The model decides when to call the tool. You then execute it and return
#   a friendly, formatted weather summary.
#
# REQUIREMENTS
# - Internet connection (for the API).
# - OPENAI_API_KEY set in your environment.
# - pip install openai requests
#
# RUN
#   python 02_weather_tool_open_meteo.py
#
# TIP
# - Try different cities by changing the user prompt. You can also add a separate
#   geocoding step (e.g., Open-Meteo geocoding) if you want to convert city names
#   to lat/lon automatically.

import os, json, requests
from openai import OpenAI

MODEL = os.getenv("MODEL", "gpt-4o-mini")
client = OpenAI()

def get_weather(lat: float, lon: float) -> dict:
    """Call Open-Meteo API for current weather and a short forecast."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m"
    )
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    # Return only what we need to keep the tool's response compact
    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "current_weather": data.get("current_weather", {}),
        "sample_hourly": data.get("hourly", {}).get("temperature_2m", [])[:6]  # first 6 hrs
    }

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather and short forecast for a coordinate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lat": {"type": "number", "description": "Latitude"},
                    "lon": {"type": "number", "description": "Longitude"}
                },
                "required": ["lat", "lon"]
            }
        }
    }
]

user_prompt = (
    "What's the weather right now in San Francisco, CA (37.7749, -122.4194)?"
    " Summarize it in a friendly sentence and include the next few hours of temperature."
)

# 1) Ask the model; it will likely call get_weather
first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": user_prompt}
    ],
    tools=tools,
    tool_choice="auto"
)

msg = first.choices[0].message
tool_messages = []

if msg.tool_calls:
    for call in msg.tool_calls:
        args = json.loads(call.function.arguments or "{}")
        result = get_weather(**args)
        tool_messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.function.name,
            "content": json.dumps(result)
        })

    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful weather assistant."},
            {"role": "user", "content": user_prompt},
            msg,
            *tool_messages
        ]
    )
    print("\n=== Weather Summary ===\n")
    print(final.choices[0].message.content)
else:
    print("Model didn't call the weather tool. Response:\n", msg.content)
