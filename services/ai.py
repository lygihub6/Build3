import os
import streamlit as st
from google import genai

def get_client():
    # try both top-level and [google] section for flexibility
    key = (
        st.secrets.get("GEMINI_API_KEY")
        or (st.secrets.get("google", {}) or {}).get("api_key")
        or os.getenv("GEMINI_API_KEY")
    )
    if not key:
        # Raise a clear message that will be caught by app.py
        raise RuntimeError(
            "Gemini API key not found. Add GEMINI_API_KEY to Streamlit secrets "
            'or set [google].api_key. Example:\nGEMINI_API_KEY = "AIzaSy...."'
        )
    return genai.Client(api_key=key)

def chat_once(messages):
    client = get_client()
    # adjust model if needed
    model = "gemini-flash-lite-latest"
    resp = client.models.generate_content(
        model=model,
        contents=messages,
        config={"temperature": 0.4},
    )
    return resp
