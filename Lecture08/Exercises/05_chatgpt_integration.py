# Exercise 5 — Integrate the OpenAI Chat Completions API
# ------------------------------------------------------
# Goal: Replace the mock response with a real ChatGPT call.
# Run with: streamlit run 05_chatgpt_integration.py
#
# Setup:
# 1) pip install openai streamlit
# 2) Set your API key in an environment variable before running:
#    macOS/Linux: export OPENAI_API_KEY="sk-..."
#    Windows (PowerShell): setx OPENAI_API_KEY "sk-..."
#
# Security note: **Never** hardcode secrets into code or commit them.

import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Exercise 5 — ChatGPT Integration", page_icon="🔌", layout="wide")
st.title("Exercise 5 — ChatGPT Integration (Chat Completions)")

# Sidebar config for model and decoding params
st.sidebar.header("Model Settings")
model = st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-5-nano"], index=0)
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max tokens", 64, 800, 256, 32)

# Show API key status (but never display the key)
if os.getenv("OPENAI_API_KEY"):
    st.sidebar.success("API key found in OPENAI_API_KEY ✔️")
else:
    st.sidebar.error("OPENAI_API_KEY not set. See comments at the top of this file.")

# Initialize OpenAI client (reads key from env var)
client = OpenAI()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful study assistant for high school students."}]

# Render chat history (skip system)
for m in st.session_state.messages:
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    elif m["role"] == "assistant":
        st.chat_message("assistant").write(m["content"])

# Chat input
if user_input := st.chat_input("Ask a study question"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        # Call the Chat Completions API
        # Reference: https://platform.openai.com/docs/api-reference/chat
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                # Only send the last ~20 messages to keep context small/cost low
                *st.session_state.messages[-20:]
            ],
        )
        assistant_text = resp.choices[0].message.content
    except Exception as e:
        assistant_text = f"API error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
    st.chat_message("assistant").write(assistant_text)

# Clear chat
if st.button("Clear chat"):
    st.session_state.messages = [{"role": "system", "content": "You are a helpful study assistant."}]
    st.rerun()
