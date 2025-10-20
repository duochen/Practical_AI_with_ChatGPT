
# Lesson 7 – Exercise 3
# Title: News Tool via Hacker News Search (no API key)
#
# GOAL
# - Practice building another tool that hits an external data source.
# - Show that tools can return structured results which the model can summarize.
#
# WHAT IT DOES
# - Uses the public HN Search API by Algolia (no key required).
# - Tool: search_hn(query, hits=5) -> returns a list of {title, url, points}.
#
# REQUIREMENTS
# - Internet connection, OPENAI_API_KEY
# - pip install openai requests
#
# RUN
#   python 03_news_tool_hn.py

import os, json, requests
from openai import OpenAI

MODEL = os.getenv("MODEL", "gpt-4o-mini")
client = OpenAI()

def search_hn(query: str, hits: int = 5) -> list:
    """Search Hacker News stories and return a compact list of results."""
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": query, "tags": "story", "hitsPerPage": hits}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    results = []
    for h in data.get("hits", []):
        results.append({
            "title": h.get("title"),
            "url": h.get("url"),
            "points": h.get("points"),
            "author": h.get("author"),
        })
    return results

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_hn",
            "description": "Search Hacker News for recent stories.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "hits": {"type": "integer", "default": 5, "minimum": 1, "maximum": 30}
                },
                "required": ["query"]
            }
        }
    }
]

user_prompt = (
    "Find interesting recent stories about 'AI in education' and summarize the top links."
    " Include bullet points with titles and URLs, and one-sentence takeaways."
)

first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful news curator."},
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
        results = search_hn(**args)
        tool_messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": call.function.name,
            "content": json.dumps(results)
        })

    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful news curator."},
            {"role": "user", "content": user_prompt},
            msg,
            *tool_messages
        ]
    )
    print("\n=== Curated Summary ===\n")
    print(final.choices[0].message.content)
else:
    print("Model didn't call the news tool. Response:\n", msg.content)
