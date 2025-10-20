
# Lesson 7 – Exercise 5
# Title: Mini CLI Assistant with Multiple Tools (Weather + Wikipedia)
#
# GOAL
# - Combine everything: multiple tools, external APIs, and nice formatting.
#
# WHAT IT DOES
# - Provides a small command-line interface:
#   > python 05_cli_tools_assistant.py "What's the weather in Seattle and a brief wiki about the city?"
# - Tools:
#   1) get_weather(lat, lon) via Open‑Meteo
#   2) wiki_summary(title) via Wikipedia REST API (no key)
#
# REQUIREMENTS
# - pip install openai requests
# - OPENAI_API_KEY in env
#
# TIP
# - If you only know the city name, ask the model to choose reasonable lat/lon.

import os, sys, json, requests
from openai import OpenAI

MODEL = os.getenv("MODEL", "gpt-4o-mini")
client = OpenAI()

def get_weather(lat: float, lon: float) -> dict:
    url = ("https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m")
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
    return {
        "timezone": data.get("timezone"),
        "current_weather": data.get("current_weather", {}),
        "hourly_next3": data.get("hourly", {}).get("temperature_2m", [])[:3]
    }

def wiki_summary(title: str) -> dict:
    # Wikipedia summary via REST API
    # Docs: https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_summary__title_
    api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
    r = requests.get(api, timeout=15, headers={"accept": "application/json"})
    if r.status_code == 404:
        return {"title": title, "summary": None, "url": None}
    r.raise_for_status()
    d = r.json()
    return {
        "title": d.get("title"),
        "summary": d.get("extract"),
        "url": d.get("content_urls", {}).get("desktop", {}).get("page")
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
                    "lat": {"type": "number"},
                    "lon": {"type": "number"}
                },
                "required": ["lat", "lon"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wiki_summary",
            "description": "Get a concise encyclopedia summary for a topic title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"}
                },
                "required": ["title"]
            }
        }
    }
]

user_text = sys.argv[1] if len(sys.argv) > 1 else (        "What's the weather in Seattle (47.6062, -122.3321)? Also give me a 2-sentence wiki summary."    )

first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a concise CLI assistant."},
        {"role": "user", "content": user_text}
    ],
    tools=tools,
    tool_choice="auto"
)

msg = first.choices[0].message
tool_msgs = []

if msg.tool_calls:
    for call in msg.tool_calls:
        args = json.loads(call.function.arguments or "{}")
        if call.function.name == "get_weather":
            out = get_weather(**args)
        elif call.function.name == "wiki_summary":
            out = wiki_summary(**args)
        else:
            out = {"error": f"Unknown tool {call.function.name}"}
        tool_msgs.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.function.name,
            "content": json.dumps(out)
        })

    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a concise CLI assistant."},
            {"role": "user", "content": user_text},
            msg,
            *tool_msgs
        ]
    )
    print(final.choices[0].message.content)
else:
    print(msg.content)
