"""
Lesson 9 – Ethics, Safety, and Responsible AI
Exercise 3: Privacy Redactor (PII patterns)

Goal:
- Detect and redact common PII patterns (emails, phone numbers, SSN-like patterns).
- Practice writing regexes and thinking about privacy by design.

How to run:
    python 3_privacy_redactor.py

What to submit:
- The redacted output and a short note on limitations (false positives/negatives).
"""

import re

sample_text = """
Hi, I'm Jamie. You can email me at jamie_smith92@example.com or call (415) 555-1234.
My backup email is jamie.smith@school.edu and my SSN is 123-45-6789 (not real).
Sometimes my number is written as 415.555.7777 or +1-415-555-8888.
"""

def redact(text: str):
    # Email
    text = re.sub(r"([A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})", "[REDACTED_EMAIL]", text)
    # Phone (very permissive demo)
    text = re.sub(r"(\+?\d[\d\-\.\s]{7,}\d)", "[REDACTED_PHONE]", text)
    # SSN-like (US)
    text = re.sub(r"\b(\d{3}-\d{2}-\d{4})\b", "[REDACTED_SSN]", text)
    return text

print("Original text:\n", sample_text)
print("\nRedacted text:\n", redact(sample_text))

print("\nNotes:")
print("- Regexes are simplistic; production systems need robust PII detectors and human review.")
print("- Always follow your school’s or organization’s privacy policy and applicable laws.")
