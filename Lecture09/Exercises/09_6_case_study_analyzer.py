"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 6 (Hands-On Lab): Case Study Analyzer

Goal:
- Analyze an AI-generated essay for factual consistency (vs. tiny KB), biased language, privacy issues, and
  similarity to known sources. Produce a compact report students can discuss in class.

How to run:
    python 6_case_study_analyzer.py

What to submit:
- The printed report and your 5–7 sentence analysis of what the author should fix and why.
"""

import re
from difflib import SequenceMatcher
from collections import Counter

# ---------- Tiny knowledge base (same style as Exercise 2) ----------
KB = {
    "water boils at sea level at 100 c": True,
    "pluto is a planet": False,
    "the pacific ocean is the largest ocean on earth": True,
}

# ---------- Demo essay (students can edit this) ----------
essay = """
In science classes, students learn that water boils at sea level at 100 C. 
Pluto is a planet everyone knows and should be taught as the ninth planet. 
The Pacific Ocean is the largest ocean on Earth. 
Contact me at alex-lee@school.edu if you need sources.
"""

# ---------- Two "sources" to compare with for similarity ----------
source_a = "Water boils at sea level at 100 C. The Pacific Ocean is the largest ocean on Earth."
source_b = "Pluto used to be called a planet, but it was reclassified as a dwarf planet in 2006 by the IAU."

# ---------- Helpers ----------
def normalize(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = s.replace(".", "")
    return s

def split_sentences(text: str):
    return [t.strip() for t in re.split(r"[.?!]\s*", text) if t.strip()]

def classify_claim(claim: str):
    key = normalize(claim)
    if key in KB:
        return "SUPPORTED" if KB[key] else "CONFLICTING"
    return "UNSUPPORTED"

def pii_redact(text: str):
    text = re.sub(r"([A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", "[REDACTED_EMAIL]", text)
    text = re.sub(r"(\+?\d[\d\-\.\s]{7,}\d)", "[REDACTED_PHONE]", text)
    return text

def char_ngrams(s: str, n: int = 5) -> set:
    s = "".join(c.lower() for c in s if not c.isspace())
    return {s[i:i+n] for i in range(max(0, len(s)-n+1))}

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)

biased_terms_pos = {"brilliant","disciplined","exceptional","hard‑working","superior"}
biased_terms_neg = {"lazy","dishonest","inferior","rude","unprepared"}

# ---------- Analysis ----------
sentences = split_sentences(essay)
facts = [(s, classify_claim(s)) for s in sentences]

# Bias scan (very naive wordlist)
tokens = re.findall(r"[A-Za-z\-]+", essay.lower())
pos_hits = [t for t in tokens if t in biased_terms_pos]
neg_hits = [t for t in tokens if t in biased_terms_neg]

# PII
pii_hits = re.findall(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", essay)
redacted = pii_redact(essay)

# Similarity vs sources
def compare(a: str, b: str):
    ng = jaccard(char_ngrams(a), char_ngrams(b))
    seq = SequenceMatcher(None, a, b).ratio()
    return ng, seq

sim_a = compare(essay, source_a)
sim_b = compare(essay, source_b)

# ---------- Report ----------
print("="*72)
print("Case Study Analyzer Report")
print("="*72)

print("\nFactual Consistency (toy KB):")
for i, (s, st) in enumerate(facts, 1):
    print(f"{i:>2}. {s}\n    ➜ {st}")

print("\nBias Language Scan (toy lexicon):")
print("  Positive-coded terms found:", pos_hits if pos_hits else "None")
print("  Negative-coded terms found:", neg_hits if neg_hits else "None")
print("  Note: Wordlists are simplistic—discuss context and intent.")

print("\nPrivacy (PII) findings:")
print("  Emails detected:", pii_hits if pii_hits else "None")
print("  Redacted preview:\n", redacted)

print("\nSimilarity Check (classroom-only):")
print(f"  vs Source A -> Jaccard: {sim_a[0]:.3f}, SeqMatch: {sim_a[1]:.3f}")
print(f"  vs Source B -> Jaccard: {sim_b[0]:.3f}, SeqMatch: {sim_b[1]:.3f}")
print("  Interpret with care; always consider citation quality and common knowledge.")

print("\nGuidance & Next Steps:")
print("- Add citations for factual claims and ensure they match reputable sources.")
print("- Replace any biased descriptors with neutral, evidence-based language.")
print("- Remove personal contact info from public drafts unless required and approved.")
print("- Include an academic honesty statement and references section.")
print("- Document your data sources, model prompts, and review process (model card + data card).")
