# Exercise 1 — Streamlit Basics & Page Layout
# -------------------------------------------
# Goal: Learn how to run a simple Streamlit app and render text, images, and layout columns.
# Run with: streamlit run 01_streamlit_intro.py
#
# What you'll practice:
# - Title, headers, markdown
# - Info/warning/success boxes
# - Columns and expanders
#
# Tip: Open http://localhost:8501 in your browser after running the command.

import streamlit as st

# --- Page config (good UX: set title, icon, and wide layout) ---
st.set_page_config(page_title="Exercise 1 — Streamlit Basics", page_icon="🤖", layout="wide")

# --- Title & intro text ---
st.title("Exercise 1 — Streamlit Basics")
st.write("This app demonstrates text blocks, layout, and basic interactivity.")

# --- Callouts help guide the user ---
st.info("Tip: Use the left ↩️ Rerun button after editing to see changes.")
st.success("✅ Streamlit is running!")

# --- Columns for simple layout ---
col1, col2 = st.columns(2)
with col1:
    st.header("Column 1")
    st.write("You can organize content into columns to improve readability.")
with col2:
    st.header("Column 2")
    st.write("Keep related widgets near each other for better UX.")

# --- Expander for optional details ---
with st.expander("Why Streamlit? (click to expand)"):
    st.markdown("""        - **Fast**: Build data/LLM apps in minutes.

    - **Pythonic**: Use familiar Python to define UI.

    - **Shareable**: Deploy easily (Streamlit Community Cloud, Hugging Face, etc.).
    """)

st.caption("End of Exercise 1 — nothing fancy yet, just clean UI scaffolding.")
