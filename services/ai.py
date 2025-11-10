# services/ai.py
import os
import streamlit as st
from google import genai
from google.genai import types

def _safe_secrets() -> dict:
    """Return secrets as a plain dict, or {} if secrets.toml is malformed."""
    try:
        # Accessing st.secrets triggers TOML parsing; wrap it.
        return dict(st.secrets)
    except Exception as e:
        # Don't crash the UI if the TOML is bad.
        print(f"[secrets] Could not parse .streamlit/secrets.toml: {e}")
        return {}

def _resolve_api_key() -> str | None:
    # 1) Prefer environment variable (avoids TOML parse entirely)
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key

    # 2) Try Streamlit secrets safely
    s = _safe_secrets()
    return s.get("GEMINI_API_KEY") or (s.get("google") or {}).get("api_key")

def get_client():
    key = _resolve_api_key()
    if not key:
        raise RuntimeError(
            "Gemini API key not found. Set an env var GEMINI_API_KEY, or fix "
            'Streamlit secrets. Example:\nGEMINI_API_KEY = "AIzaSy...."  (quotes required)'
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
