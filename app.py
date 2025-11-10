
# app.py
import streamlit as st
from state import get_state
from ui.components import inject_css, shell_left, chat_card
from steps import REGISTRY
from services.ai import chat_once
from google.genai import types

st.set_page_config(page_title="Sylvia – Learning Facilitator", page_icon="🎓", layout="wide")
inject_css()

state = get_state(st)
shell_left(st, state)

# 3-column shell
_, main, _ = st.columns([1,3,1])

with main:
    st.title("📚 Sylvia – Your Learning Facilitator")
    # render the active step
    step = REGISTRY.get(state.current_step)
    if step is None:
        st.warning("Unknown step. Resetting to Goals.")
        state.current_step = "goals"
        step = REGISTRY["goals"]
    step.render(st, state)

    st.markdown("---")
    # shared chat (optional)
    user_text = chat_card(st, state)
    if user_text:
        state.messages.append({"role":"user","content":user_text})
        # minimal history -> Gemini parts
        parts = [types.Content(role=("user" if m["role"]=="user" else "model"),
                               parts=[types.Part(text=m["content"])])
                 for m in state.messages[-10:]]
        try:
            resp = chat_once(parts)
            text = resp.text or "I’m here to help."
            state.messages.append({"role":"assistant","content":text})
            st.rerun()
        except Exception as e:
            state.messages.append({"role":"assistant","content":f"Error: {e}"})
            st.rerun()
