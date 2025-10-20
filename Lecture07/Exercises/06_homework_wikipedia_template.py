
# Lesson 7 – Homework Template
# Title: Replace the Weather Tool with a Different API (Wikipedia or Dictionary)
#
# INSTRUCTIONS
# 1) Choose ONE API: Wikipedia summary (no key) or Free Dictionary (free, no key).
# 2) Implement a tool function (e.g., wiki_summary(title) or define_word(term)).
# 3) Ask the model a question that should trigger the tool.
# 4) Print a clean, human-friendly answer.
#
# EXAMPLE BELOW (Wikipedia). For a dictionary, see note at bottom.
#
# RUN
#   python 06_homework_wikipedia_template.py
#
# BONUS
# - Add error handling for 404s or missing fields.
# - Add a second tool and let the model decide which one to call.

import os, json, requests
from openai import OpenAI

MODEL = os.getenv("MODEL", "gpt-4o-mini")
client = OpenAI()

def wiki_summary(title: str) -> dict:
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

user_prompt = "Give me a brief encyclopedia summary of 'reinforcement learning' in 2 sentences."

first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful research assistant."},
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
        result = wiki_summary(**args)
        tool_messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.function.name,
            "content": json.dumps(result)
        })
    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": user_prompt},
            msg,
            *tool_messages
        ]
    )
    print("\n=== Summary ===\n")
    print(final.choices[0].message.content)
else:
    print("Model didn't call the wiki tool. Response:\n", msg.content)

# DICTIONARY OPTION (idea)
# Instead of wiki_summary, implement:
#   def define_word(term: str) -> dict:
#       url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
#       ... parse meanings and examples ...
# Then register it as a tool named "define_word" and ask the model
# to "Define '<term>' and provide one example sentence."
