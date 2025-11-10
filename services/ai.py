
# services/ai.py
import streamlit as st
from google import genai
from google.genai import types

@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY missing in st.secrets")
    return genai.Client(api_key=api_key)

def load_identity():
    try:
        return open("identity.txt").read()
    except FileNotFoundError:
        return ("You are Sylvia, a learning facilitator… "
                "Follow: goals → task analysis → strategies → time plan → resources → reflect → feedback.")

def get_config():
    return types.GenerateContentConfig(
        system_instruction=load_identity(),
        temperature=0.7,
        max_output_tokens=2048,
    )

def chat_once(history_parts):
    client = get_client()
    cfg = get_config()
    return client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=history_parts,
        config=cfg,
    )
