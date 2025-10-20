"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 5: Prompt Safety Guardrails (keyword demo)

Goal:
- Build a simple rules-based filter that blocks unsafe prompts (e.g., cheating, targeted harassment, PII scraping).
- Show allow vs. block decisions with explanations.

How to run:
    python 5_guardrails_demo.py

What to submit:
- A screenshot or copy of the decisions and a 3–4 sentence note on why rules + humans-in-the-loop are both needed.
"""

from typing import List, Tuple

BLOCKLIST = {
    "cheating": ["answer the exam", "write my test", "give me the quiz answers"],
    "harassment": ["insult", "bully", "humiliate", "targeted harassment"],
    "weapons": ["make a bomb", "buy a gun for me"],
    "pii-scrape": ["find their password", "steal credit card", "ssn list", "social security list"],
}

ALLOWLIST = [
    "study guide", "practice problems", "how to improve", "learn safely", "classroom policy"
]

def decision(prompt: str) -> Tuple[str, str]:
    p = prompt.lower()
    # Allowlist first
    if any(kw in p for kw in ALLOWLIST):
        return "ALLOW", "Matches allowlist for helpful/educational intent."
    # Blocklist categories
    for category, kws in BLOCKLIST.items():
        if any(kw in p for kw in kws):
            return "BLOCK", f"Unsafe intent detected: '{category}' keywords."
    return "REVIEW", "No explicit flags, but send to human review if sensitive."

test_prompts = [
    "Make me a study guide for tomorrow's algebra test.",
    "Can you answer the exam for me? It's multiple choice.",
    "Find their password from the school network dump.",
    "How to learn safely about lab chemicals and avoid accidents?",
    "Tell me the quiz answers now.",
    "Generate some practice problems on responsible AI."
]

print("Prompt Safety Guardrails Demo\n")
for t in test_prompts:
    d, why = decision(t)
    print(f"Prompt: {t}\n  Decision: {d}\n  Reason: {why}\n")

print("Notes:")
print("- Rules are brittle; combine with model classifiers, rate limiting, and human oversight.")
print("- Log decisions; review edge cases to improve your policy.")
