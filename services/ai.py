# services/ai.py
import os
import streamlit as st
from google import genai
from google.genai import types

@st.cache_resource
def get_client():
    # Accept several shapes: top-level, [google] section, or env var
    key = (
        st.secrets.get("GEMINI_API_KEY")
        or (st.secrets.get("google", {}) or {}).get("api_key")
        or os.getenv("GEMINI_API_KEY")
    )
    if not key:
        raise RuntimeError(
            "Gemini API key not found. Add GEMINI_API_KEY to secrets or use:\n"
            'GEMINI_API_KEY = "AIzaSy..."  (quotes required)'
        )
    return genai.Client(api_key=key)

def load_identity():
    try:
        with open("identity.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return "You are Sylvia, a self-regulated learning facilitator."

def get_config():
    return types.GenerateContentConfig(
        system_instruction=load_identity(),
        temperature=0.4,
        max_output_tokens=2048,
    )

def chat_once(history_parts):
    client = get_client()
    return client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=history_parts,
        config=get_config(),
    )
