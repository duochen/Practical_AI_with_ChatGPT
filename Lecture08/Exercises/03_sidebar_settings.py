# Exercise 3 — Sidebar Settings (UX Pattern)
# ------------------------------------------
# Goal: Add a sidebar with global controls/settings that affect app behavior.
# Run with: streamlit run 03_sidebar_settings.py

import streamlit as st

st.set_page_config(page_title="Exercise 3 — Sidebar Settings", page_icon="🎚️", layout="wide")
st.title("Exercise 3 — Sidebar Settings")

# Sidebar: common place for global controls (model, temperature, max_tokens, theme, etc.)
st.sidebar.header("Settings")
temperature = st.sidebar.slider("Creativity (temperature)", 0.0, 2.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max tokens", 64, 800, 256, 32)
show_tips = st.sidebar.checkbox("Show usage tips", True)

st.write(f"**Temperature:** {temperature} | **Max tokens:** {max_tokens}")

if show_tips:
    st.info("Tip: The sidebar helps keep your main area focused on the conversation.")

# Main area content
st.subheader("Main Content")
prompt = st.text_area("Enter a prompt:", height=120, placeholder="Write a paragraph about why UX matters for AI tools.")
if st.button("Generate (mock)"):
    st.write("This is a placeholder. We'll integrate the API next.")

st.caption("Good UX: settings on the left, task area on the right.")
