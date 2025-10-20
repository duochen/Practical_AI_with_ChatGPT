
# Lesson 7 – Exercise 4
# Title: Structured Outputs (JSON) + Validation
#
# GOAL
# - Get the model to emit STRICT JSON for a known schema.
# - Validate the JSON using Python (jsonschema) so downstream code is robust.
#
# WHAT IT DOES
# - Prompts the model to return a fixed schema for a "WeatherReport".
# - Tries to parse JSON; if invalid, asks the model to correct itself.
#
# REQUIREMENTS
# - pip install openai jsonschema
# - OPENAI_API_KEY in env
#
# RUN
#   python 04_structured_output_validation.py

import os, json
from openai import OpenAI
from jsonschema import validate, ValidationError

MODEL = os.getenv("MODEL", "gpt-4o-mini")
client = OpenAI()

schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "summary": {"type": "string"},
        "temp_c": {"type": "number"},
        "hourly_c": {
            "type": "array",
            "items": {"type": "number"}
        }
    },
    "required": ["location", "summary", "temp_c", "hourly_c"],
    "additionalProperties": False
}

system = (
    "You are a formatter that outputs ONLY JSON and nothing else.\n"
    "If you are unsure, make a best effort.\n"
    "Do not wrap in markdown. Do not include comments."
)
user = (
    "Create a WeatherReport JSON for 'Austin, TX' with a short textual summary,"
    " a current temperature in Celsius, and 5 hourly temps."
)

def ask_for_json():
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
            {"role": "user", "content": "Schema:"},
            {"role": "user", "content": json.dumps(schema)}
        ]
    )
    return resp.choices[0].message.content

raw = ask_for_json()
try:
    data = json.loads(raw)
    validate(instance=data, schema=schema)
    print("\nValid JSON received:\n", json.dumps(data, indent=2))
except (json.JSONDecodeError, ValidationError) as e:
    print("First attempt invalid, asking the model to fix it...\nReason:", e)
    fix_prompt = (
        "Your previous output was invalid. Return ONLY valid JSON that matches this schema:"
        f"\n{json.dumps(schema)}\nPrevious output:\n{raw}"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": fix_prompt}
        ]
    )
    corrected = resp.choices[0].message.content
    data = json.loads(corrected)
    validate(instance=data, schema=schema)
    print("\nCorrected valid JSON:\n", json.dumps(data, indent=2))
