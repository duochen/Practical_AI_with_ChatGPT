"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 1: Mini Bias Audit on Text Snippets

Goal:
- Detect potential stereotyping or sentiment skew across two groups using a tiny lexicon.
- Practice calculating simple bias indicators and writing a short reflection.

How to run:
    python 1_bias_audit.py

What to submit:
- The printed report and, in a separate note, 3–5 sentences interpreting the results:
  * Is there a skew? What might cause it?
  * How could we improve the audit? (e.g., bigger lexicons, more data, better sentiment analysis)
"""

from collections import Counter
import re

# ---------------------
# Sample mini‑dataset (toy examples for classroom use)
# You can add/remove sentences to experiment.
# ---------------------
sentences = [
    "GroupA students are brilliant, creative, and disciplined.",
    "GroupB students are lazy and not very capable.",
    "I met two GroupA students who were helpful and motivated.",
    "Some GroupB students were troublesome and dishonest.",
    "GroupA team was polite, friendly, and hard‑working.",
    "GroupB team seemed rude and unprepared.",
]

# ---------------------
# Very small adjective lexicon to illustrate the idea
# (In real audits you’d use larger, validated lexicons.)
# ---------------------
positive_words = {
    "brilliant","creative","disciplined","helpful","motivated",
    "polite","friendly","hard‑working","capable","prepared"
}
negative_words = {
    "lazy","not","troublesome","dishonest","rude","unprepared"
}

# Groups we want to compare
groups = ["GroupA", "GroupB"]

def tokenize(text: str):
    """Lowercase word tokenizer (very simple)."""
    return re.findall(r"[A-Za-z\-]+", text.lower())

def sentence_group(sentence: str):
    """Return which group the sentence targets (GroupA or GroupB) or None."""
    for g in groups:
        if g.lower() in sentence.lower():
            return g
    return None

def sentiment_counts(tokens):
    """Count positive/negative words using our tiny lexicon."""
    pos = sum(1 for t in tokens if t in positive_words)
    neg = sum(1 for t in tokens if t in negative_words)
    return pos, neg

# Collect stats per group
stats = {g: Counter(pos=0, neg=0, total_tokens=0, sentences=0) for g in groups}

for s in sentences:
    g = sentence_group(s)
    if not g:
        continue
    tokens = tokenize(s)
    pos, neg = sentiment_counts(tokens)
    stats[g]["pos"] += pos
    stats[g]["neg"] += neg
    stats[g]["total_tokens"] += len(tokens)
    stats[g]["sentences"] += 1

# Compute simple metrics
def safe_div(a, b):
    return (a / b) if b else 0.0

print("="*70)
print("Mini Bias Audit Report")
print("="*70)
for g in groups:
    pos = stats[g]["pos"]
    neg = stats[g]["neg"]
    sent = stats[g]["sentences"]
    total_tokens = stats[g]["total_tokens"]
    pos_rate = safe_div(pos, total_tokens)
    neg_rate = safe_div(neg, total_tokens)
    net_sentiment = pos - neg
    print(f"\nGroup: {g}")
    print(f"  Sentences        : {sent}")
    print(f"  Tokens           : {total_tokens}")
    print(f"  Positive matches : {pos}")
    print(f"  Negative matches : {neg}")
    print(f"  Pos rate         : {pos_rate:.3f}")
    print(f"  Neg rate         : {neg_rate:.3f}")
    print(f"  Net sentiment    : {net_sentiment:+d} (pos - neg)")

# Very naive fairness flag
gap = (stats["GroupA"]["pos"] - stats["GroupA"]["neg"]) - (stats["GroupB"]["pos"] - stats["GroupB"]["neg"])
print("\nOverall net‑sentiment gap (GroupA - GroupB):", f"{gap:+d}")
if gap > 0:
    print("⚠️  Potential positive skew toward GroupA (toy example).")
elif gap < 0:
    print("⚠️  Potential positive skew toward GroupB (toy example).")
else:
    print("No net difference detected (on this tiny sample).")

print("\nNotes:")
print("- This is a tiny, toy lexicon and dataset. Real audits use larger corpora, better NLP, and human review.")
print("- Avoid essentializing groups; focus on improving data quality and annotation practices.")
