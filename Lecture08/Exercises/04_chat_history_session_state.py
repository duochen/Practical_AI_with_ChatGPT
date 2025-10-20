# Exercise 4 — Chat History with st.session_state
# -----------------------------------------------
# Goal: Maintain conversation state (messages) across reruns.
# Run with: streamlit run 04_chat_history_session_state.py

import streamlit as st

st.set_page_config(page_title="Exercise 4 — Chat History", page_icon="💬", layout="wide")
st.title("Exercise 4 — Chat History with session_state")

# Initialize a list in session_state to store messages (role, content)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me anything about your studies."}]

# Render chat history
for m in st.session_state.messages:
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    else:
        st.chat_message("assistant").write(m["content"])

# Chat input (bottom)
if prompt := st.chat_input("Type your message"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Mock assistant reply; real LLM will replace this later
    reply = "Thanks! (Mock) I will answer more fully once the API is connected."
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

# Clear history button (useful for testing)
if st.button("Clear chat history"):
    st.session_state.messages = []
    st.rerun()
