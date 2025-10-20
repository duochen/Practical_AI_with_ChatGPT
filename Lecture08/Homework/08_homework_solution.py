
# 07_homework_solution.py
# -------------------------------------------------------------
# Slide 29 – Homework Solution
# - Add a "study topic" dropdown for preset prompts
# - Include an option to summarize notes (upload text file)
# - Optional: Deployment tips in the sidebar
#
# Run: streamlit run 07_homework_solution.py
#
# Requirements:
#   pip install streamlit openai
#   export OPENAI_API_KEY="sk-..."

import os
import streamlit as st
from openai import OpenAI

# ---------- Page Setup ----------
st.set_page_config(page_title="Homework — Study Assistant Enhancements", page_icon="🧰", layout="wide")
st.title("🧰 Homework Solution — Study Assistant Enhancements")
st.caption("Implements: study topic presets + note summarizer + deployment tips")

# ---------- Sidebar: Settings & Deployment Tips ----------
with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-5-nano"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max tokens", 64, 1200, 400, 16)

    st.divider()
    st.subheader("Deployment tips")
    st.markdown("""
    **Streamlit Community Cloud**
    1. Push your app file(s) to a public GitHub repo.
    2. Go to **share.streamlit.io** and select your repo/branch/app file.
    3. Add **OPENAI_API_KEY** as a *secret* in the app settings.

    **Hugging Face Spaces**
    1. Create a new *Space* → SDK: *Streamlit*.
    2. Upload your files. In *Settings → Secrets*, add **OPENAI_API_KEY**.
    3. Set *App File*: `07_homework_solution.py`.
    """)

    if os.getenv("OPENAI_API_KEY"):
        st.success("OPENAI_API_KEY detected ✔️")
    else:
        st.warning("Set OPENAI_API_KEY in your environment before calling the API.")

# Initialize OpenAI
client = OpenAI()

# ---------- Session State (Chat History) ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a concise, kind study assistant for middle and high school students."}
    ]

# ---------- Study Topic Presets ----------
st.subheader("🎯 Study Topic Presets")
presets = {
    "Algebra — Quadratic Equations": "Explain how to solve quadratic equations by factoring, completing the square, and using the quadratic formula. Give one short example for each method.",
    "Biology — Cell Organelles": "Explain the major cell organelles (nucleus, ribosomes, mitochondria, ER, Golgi, lysosomes, chloroplasts) with a one-line function for each and a quick analogy.",
    "Chemistry — Stoichiometry": "Explain stoichiometry basics with a small example converting grams to moles to molecules. Show the steps clearly.",
    "Physics — Newton’s Laws": "Explain Newton’s three laws with one real-life example for each, then give a 2-question practice quiz with answers.",
    "Python — Lists vs. Dictionaries": "Compare Python lists and dictionaries. Show when to use each, with commented code examples and a short exercise.",
    "U.S. History — Bill of Rights": "Summarize the Bill of Rights in plain language with one practical example per amendment.",
    "Custom": ""
}

topic = st.selectbox("Choose a topic:", list(presets.keys()))
preset_prompt = presets[topic]
custom_prompt = st.text_area("Prompt (editable)", value=preset_prompt, height=140, placeholder="Write your study request...")

cols = st.columns(2)
with cols[0]:
    if st.button("Generate Study Guide"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": custom_prompt})
        with st.spinner("Generating..."):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=st.session_state.messages[-24:],
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                answer = f"API error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.success("Response generated below.")
with cols[1]:
    if st.button("Clear Chat"):
        st.session_state.messages = st.session_state.messages[:1]  # keep system prompt
        st.toast("Chat cleared.")

# ---------- Notes Summarizer (Upload) ----------
st.subheader("🗂️ Summarize Your Notes (Upload .txt / .md)")
uploaded = st.file_uploader("Upload a text file", type=["txt", "md"])

colA, colB = st.columns(2)
with colA:
    detail = st.radio("Summary detail level", ["Brief (5 bullets)", "Concise (~150 words)", "Detailed (~300 words)"], index=1)
with colB:
    tone = st.radio("Audience", ["Middle school", "High school"], index=1)

summary_request = f"Summarize the student's notes at a {detail.lower()} level for a {tone.lower()} audience. Include 1–2 examples if appropriate."

if uploaded and st.button("Summarize Notes"):
    try:
        text = uploaded.read().decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    if not text.strip():
        st.error("Couldn't read file or file is empty.")
    else:
        prompt = f"{summary_request}\n\n---\nNotes:\n{text[:12000]}"  # safety: limit size
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Summarizing..."):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    messages=st.session_state.messages[-24:],
                )
                summary = resp.choices[0].message.content
            except Exception as e:
                summary = f"API error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": summary})
        st.success("Summary generated below.")

# ---------- Render Chat History ----------
st.subheader("💬 Conversation")
for m in st.session_state.messages[1:]:  # skip system
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    else:
        st.chat_message("assistant").write(m["content"])

st.caption("Tip: Keep prompts short and focused. Upload notes in .txt or .md for best results.")
