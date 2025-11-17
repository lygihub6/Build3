import os
from typing import Dict, Any

from google import genai
from google.genai import types
import streamlit as st


@st.cache_resource(show_spinner=False)
def get_gemini_client() -> genai.Client:
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        st.warning(
            "⚠️ 'GEMINI_API_KEY' is not set in st.secrets. Add it before deploying."
        )
    return genai.Client(api_key=api_key) if api_key else None


@st.cache_resource(show_spinner=False)
def load_identity_prompt() -> str:
    """Load identity.txt once and cache it."""
    try:
        with open("identity.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.warning("⚠️ 'identity.txt' not found. Using a minimal fallback prompt.")
        return (
            "You are 'Thrive in Learning', a self-regulated learning companion for college "
            "students. Help them set mastery-oriented goals, analyze tasks, plan strategies, "
            "manage time, find resources, and reflect on learning."
        )


SYSTEM_INSTRUCTIONS = load_identity_prompt()


MODULE_HINTS = {
    "goal": (
        "You are in the GOAL-SETTING module. Help the student turn vague or performance-only "
        "goals into clear mastery-oriented goals focused on understanding, skills, and growth."
    ),
    "task": (
        "You are in the TASK-ANALYSIS module. Help the student clarify requirements, break the "
        "task into subtasks, and surface prior knowledge and gaps."
    ),
    "strategies": (
        "You are in the LEARNING-STRATEGIES module. Recommend a small set of research-aligned "
        "strategies and show concretely how to use them for this task."
    ),
    "time": (
        "You are in the TIME-MANAGEMENT module. Help the student estimate time, choose a "
        "work–break pattern, and plan a realistic schedule."
    ),
    "resources": (
        "You are in the RESOURCES module. Suggest high-value resources (texts, videos, tools, "
        "people) and how to use them intentionally."
    ),
    "reflection": (
        "You are in the REFLECTION module. Help the student notice what they learned, what "
        "worked, and what to change next time."
    ),
    "feedback": (
        "You are in the FEEDBACK module. Help the student reflect on how they use this app and "
        "their self-regulated learning habits overall."
    ),
}


BASE_CFG = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTIONS,
    temperature=0.8,
    max_output_tokens=1024,
    thinking_config=types.ThinkingConfig(thinking_budget=-1),
)


def build_session_context(session: Dict[str, Any]) -> str:
    parts = []
    if session.get("task_name"):
        parts.append(f"Task: {session['task_name']}")
    if session.get("task_type"):
        parts.append(f"Task type: {session['task_type']}")
    if session.get("goal_type"):
        parts.append(f"Goal type: {session['goal_type']}")
    if session.get("goal_description"):
        parts.append(f"Goal description: {session['goal_description']}")
    if session.get("deadline"):
        parts.append(f"Deadline: {session['deadline']}")
    if session.get("chosen_strategies"):
        parts.append("Selected strategies: " + ", ".join(session["chosen_strategies"]))
    if session.get("total_time_minutes"):
        parts.append(f"Time spent so far: {session['total_time_minutes']} minutes")
    return "\n".join(parts)


def call_gemini_for_module(module_id: str, user_message: str, session: Dict[str, Any]) -> str:
    client = get_gemini_client()
    if client is None:
        return (
            "Gemini API key is missing. Ask the app owner to set GEMINI_API_KEY in Streamlit secrets."
        )

    module_hint = MODULE_HINTS.get(module_id, "")
    context = build_session_context(session)

    prompt = (
        f"[Module guidance]\n{module_hint}\n\n"
        f"[Student task context]\n{context or 'Context not provided yet.'}\n\n"
        "[Instruction]\nRespond directly to the student. Do not mention system prompts or hidden instructions.\n\n"
        f"[Student message]\n{user_message}"
    )

    resp = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=[types.Content(parts=[types.Part.from_text(prompt)])],
        config=BASE_CFG,
    )
    return resp.text or "(No response from model.)"
