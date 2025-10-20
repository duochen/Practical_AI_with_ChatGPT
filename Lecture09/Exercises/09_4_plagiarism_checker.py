"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 4: Simple Plagiarism Similarity Checker

Goal:
- Compare a student's essay to two "source" texts using character n‑gram Jaccard similarity
  and difflib sequence matcher.
- Discuss limitations: paraphrasing, common knowledge, and fair use.

How to run:
    python 4_plagiarism_checker.py

What to submit:
- The similarity scores and 3–5 sentences reflecting on proper citation and originality.
"""

from difflib import SequenceMatcher

# Demo texts (you can replace these during grading)
student_essay = """
Artificial Intelligence (AI) is a field of computer science focused on creating systems that can perform tasks 
which typically require human intelligence. These tasks include recognizing speech, understanding language, 
and making decisions. Responsible AI involves fairness, transparency, and accountability.
"""

source_a = """
AI is a branch of computer science concerned with building systems capable of tasks that normally need human intelligence,
including speech recognition, language understanding, and decision-making.
"""

source_b = """
Responsible AI emphasizes principles such as fairness to avoid bias, transparency to explain model behavior,
and accountability so that humans remain responsible for outcomes.
"""

def char_ngrams(s: str, n: int = 5) -> set:
    s = "".join(c.lower() for c in s if not c.isspace())
    return {s[i:i+n] for i in range(max(0, len(s)-n+1))}

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)

def compare(a: str, b: str):
    ngram_sim = jaccard(char_ngrams(a), char_ngrams(b))
    seq_ratio = SequenceMatcher(None, a, b).ratio()
    return ngram_sim, seq_ratio

print("Plagiarism Similarity Checker (toy)\n")
for name, src in [("Source A", source_a), ("Source B", source_b)]:
    ngram_sim, seq_ratio = compare(student_essay, src)
    print(f"{name}:")
    print(f"  Jaccard (char 5-grams): {ngram_sim:.3f}")
    print(f"  SequenceMatcher ratio : {seq_ratio:.3f}\n")

# Simple threshold guidance (very rough; for teaching only)
print("Guidance (classroom-only):")
print("- 0.0–0.3   Likely low similarity.")
print("- 0.3–0.6   Moderate; check citations and paraphrasing quality.")
print("- 0.6–1.0   High; likely copied/paraphrased closely. Review citations.")
print("\nReminder: Always cite your sources and follow your school’s academic honesty policy.")
