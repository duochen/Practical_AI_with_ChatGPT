# Exercise 6 — ChatGPT Study Assistant (End-to-End App)
# -----------------------------------------------------
# Goal: Build a study Q&A assistant with sidebar settings, chat history, and helpful prompts.
# Run with: streamlit run 06_study_assistant_app.py

import os
from datetime import datetime
import streamlit as st
from openai import OpenAI

# ---- Page & Sidebar ----
st.set_page_config(page_title="Study Assistant — Lesson 8", page_icon="📚", layout="wide")
st.title("📚 ChatGPT Study Assistant")
st.caption("Lesson 8 — Building a ChatGPT Web App with Streamlit")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-5-nano"], index=0)
    temperature = st.slider("Creativity (temperature)", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max tokens", 64, 1200, 300, 16)
    system_prompt = st.text_area(
        "System behavior",
        value=(
            "You are a kind, concise study assistant for middle and high school students. "
            "When asked for an explanation, use simple language and short examples. "
            "When asked for code, provide commented snippets."
        ),
        height=100,
    )
    show_timestamps = st.checkbox("Show timestamps", True)
    st.divider()
    st.caption("API key must be set in the environment variable OPENAI_API_KEY.")
    if os.getenv("OPENAI_API_KEY"):
        st.success("API key detected ✔️")
    else:
        st.error("OPENAI_API_KEY not set")

client = OpenAI()

# ---- Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Update system message dynamically if changed in the sidebar
# (Replace the first system message content to keep history stable)
if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
    st.session_state.messages[0]["content"] = system_prompt

# ---- Helper: render chat history (skip system) ----
def render_history():
    for m in st.session_state.messages[1:]:
        if m["role"] == "user":
            st.chat_message("user").write(m["content"])
        elif m["role"] == "assistant":
            if show_timestamps and "timestamp" in m:
                st.chat_message("assistant").write(f"{m['content']}\n\n_{m['timestamp']}_")
            else:
                st.chat_message("assistant").write(m["content"])

render_history()

# ---- Chat Input ----
if prompt := st.chat_input("Ask a study question (math, science, programming, etc.)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Send only the recent window to control latency/cost
        window = st.session_state.messages[-24:]
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=window,
        )
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = f"API error: {e}"

    # Add metadata like a timestamp to the assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })
    st.chat_message("assistant").write(answer)

# ---- Tools/Shortcuts under the chat ----
with st.expander("Helpful prompts for students"):
    st.markdown("""
    - *Explain like I'm 12:* Explain [TOPIC] in simple terms with a short example.

    - *Study guide:* Create a 5-bullet study guide for [TOPIC].

    - *Practice quiz:* Ask me 3 questions about [TOPIC] and check my answers.

    - *Debug help:* I have this error: `[paste error]`. What's likely wrong?
    """)

# ---- Footer actions ----
cols = st.columns(3)
if cols[0].button("Clear chat"):
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.rerun()
if cols[1].button("Insert example question"):
    example = "Explain the difference between precision and recall with a tiny example."
    st.session_state.messages.append({"role": "user", "content": example})
    st.rerun()
if cols[2].button("Copy latest answer to clipboard"):
    # Streamlit can't write to the OS clipboard directly; show instructions instead.
    st.toast("Select the answer text and press Ctrl/Cmd+C to copy.")
