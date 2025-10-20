"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 2: Hallucination / Fact Consistency Checker (toy)

Goal:
- Given a short model‑generated passage, identify claims and compare to a small "ground truth" knowledge base.
- Mark claims as SUPPORTED, UNSUPPORTED, or CONFLICTING.

How to run:
    python 2_hallucination_checker.py

What to submit:
- The printed table and 2–4 sentences on how you would reduce hallucinations in your workflow.
"""

import re
from textwrap import wrap

# ---------------------
# Tiny knowledge base (classroom demo only)
# ---------------------
KB = {
    "water boils at sea level at 100 c": True,
    "the great wall of china is visible from space with the naked eye": False,
    "python was first released in 1991": True,
    "pluto is a planet": False,  # reclassified as dwarf planet in 2006
    "the pacific ocean is the largest ocean on earth": True,
}

# ---------------------
# Sample model output (students can edit and test different passages)
# ---------------------
generated_text = (
    "Water boils at sea level at 100 C. "
    "The Great Wall of China is visible from space with the naked eye. "
    "Python was first released in 1991. "
    "Pluto is a planet in our solar system. "
    "The Pacific Ocean is the largest ocean on Earth."
)

def normalize(s: str) -> str:
    """Lowercase and basic cleanup for matching to KB keys."""
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace(".", "")
    return s

def split_sentences(text: str):
    # Very basic sentence split by period; robust tokenizers are better.
    return [t.strip() for t in re.split(r"[.?!]\s*", text) if t.strip()]

def classify_claim(claim: str):
    key = normalize(claim)
    if key in KB:
        return "SUPPORTED" if KB[key] else "CONFLICTING"
    return "UNSUPPORTED"

claims = split_sentences(generated_text)

print("="*72)
print("Hallucination / Fact Consistency Checker (Toy Demo)")
print("="*72)
print("\nKnowledge Base facts (keys):")
for k, v in KB.items():
    print(f"  - {k}  -> {'True' if v else 'False'}")

print("\nAnalyzing generated text:\n")
for idx, c in enumerate(claims, 1):
    status = classify_claim(c)
    print(f"{idx:>2}. {c}")
    print(f"    ➜ {status}")
print("\nLegend: SUPPORTED = matches KB; CONFLICTING = contradicts KB; UNSUPPORTED = not in KB")

print("\nReflection prompts:")
print("- How would you reduce hallucinations (e.g., retrieval, citing sources, chain‑of‑thought verification)?")
print("- When is it acceptable to say 'I don't know' or ask for clarification?")
