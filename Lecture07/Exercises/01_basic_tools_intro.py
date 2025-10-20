
# Lesson 7 – Exercise 1
# Title: Zero-to-One Function Calling (No external API)
#
# GOAL
# - Understand the idea of "tools" (aka function calling) with ChatGPT.
# - We register Python functions as tools; the model decides when to call them.
# - This example stays 100% local (no web calls) so you can run it anywhere.
#
# WHAT IT DOES
# - Exposes two tiny math utilities as "tools" for the model to call:
#   add(a, b) and stats(numbers).
# - Sends a user question to the model; if the model needs a tool, it will
#   return a tool call which we execute, then we send the result back.
#
# REQUIREMENTS
# - Set environment variable OPENAI_API_KEY before running:
#     mac/linux: export OPENAI_API_KEY=sk-... 
#     windows  : setx OPENAI_API_KEY sk-...
# - pip install openai (>=1.0) if you haven't already.
#
# RUN
#   python 01_basic_tools_intro.py
#
# NOTES
# - Keep the MODEL name configurable via an env var (MODEL).
# - This script is intentionally verbose with comments for teaching.

import os, json, math
from typing import List, Dict, Any
try:
    # Newer OpenAI SDK (recommended)
    from openai import OpenAI
    client = OpenAI()
except Exception:
    # Fallback for older SDKs: pip install openai==1.x is recommended.
    raise SystemExit("Please install the new OpenAI SDK: pip install openai")

MODEL = os.getenv("MODEL", "gpt-4o-mini")  # use a fast, inexpensive model by default

# -------------------------
# 1) Define Python functions that will be exposed as tools
# -------------------------
def add(a: float, b: float) -> float:
    """Return a + b."""
    return a + b

def stats(numbers: list) -> dict:
    """Return simple statistics for a list of numbers."""
    if not numbers:
        return {"count": 0, "mean": None, "stdev": None}
    mean = sum(numbers) / len(numbers)
    if len(numbers) > 1:
        var = sum((x - mean)**2 for x in numbers) / (len(numbers)-1)
        stdev = math.sqrt(var)
    else:
        stdev = 0.0
    return {"count": len(numbers), "mean": mean, "stdev": stdev}

# -------------------------
# 2) Register tools for the model
# -------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two numbers and return the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stats",
            "description": "Compute count, mean, and stdev for a list of numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numbers": {
                        "type": "array",
                        "items": {"type": "number"}
                    }
                },
                "required": ["numbers"]
            }
        }
    }
]

# -------------------------
# 3) Chat loop (single turn) demonstrating tool use
# -------------------------
user_prompt = (
    "I have numbers 2, 4, 6, 8. First add 2 and 8, then show stats for the full list."
)

# We send the user's request; the model may respond with a tool call.
first = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
    ],
    tools=tools,
    tool_choice="auto"  # let the model decide
)

# The model might produce one or more tool_calls in 'message'
msg = first.choices[0].message
tool_results_messages = []

if msg.tool_calls:
    # Execute each tool call in the order given
    for call in msg.tool_calls:
        name = call.function.name
        args = json.loads(call.function.arguments or "{}")

        if name == "add":
            result = add(**args)
        elif name == "stats":
            result = stats(**args)
        else:
            result = {"error": f"Unknown tool: {name}"}

        # Append a 'tool' message back to the model with the result
        tool_results_messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "name": name,
            "content": json.dumps(result)
        })

    # Send a follow-up message containing the tool results so the model can finalize an answer
    final = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt},
            msg,  # the model's tool-call message
            *tool_results_messages
        ]
    )
    print("\n=== Final Answer ===\n")
    print(final.choices[0].message.content)
else:
    # No tool call needed; the model answered directly
    print("\n=== Answer (no tools needed) ===\n")
    print(msg.content)
