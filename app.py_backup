
# app.py
import streamlit as st
from state import get_state

# Components we actually have
from ui.components import inject_css, chat_card

# Steps registry (safe import)
try:
    from steps import REGISTRY
except Exception as e:
    REGISTRY = {}
    # We'll still render a chat-only fallback
    print(f"[app] Steps failed to load: {e}")

# AI call (safe import + graceful fallback)
try:
    from services.ai import chat_once
    _ai_ok = True
except Exception as e:
    print(f"[app] AI service unavailable: {e}")
    _ai_ok = False

st.set_page_config(page_title="Sylvia – Learning Facilitator", page_icon="🎓", layout="wide")

def main():
    state = get_state(st)
    inject_css()

    # --- Layout ------------------------------------------------------------
    left, main = st.columns([1, 2], gap="large")

    # Left: simple nav using whatever steps loaded successfully
    with left:
        st.markdown("### 🧭 Steps")
        if REGISTRY:
            labels = [f"{m.icon} {m.label}" for m in REGISTRY.values()]
            keys = list(REGISTRY.keys())
            idx = keys.index(state.current_step) if state.current_step in keys else 0
            choice = st.radio(
                "Workflow",
                labels,
                index=idx,
                label_visibility="collapsed",
            )
            # map back to step key
            state.current_step = keys[labels.index(choice)]
        else:
            st.info("No step modules available. Chat is still available below.")

        # show current goals if any
        if getattr(state, "learning_goals", None):
            st.markdown("#### 🎯 Your Goals")
            for i, g in enumerate(state.learning_goals, 1):
                st.write(f"{i}. {g}")

    # Main: render step or fallback
    with main:
        st.title("📚 Sylvia – Your Learning Facilitator")

        if REGISTRY and state.current_step in REGISTRY:
            step = REGISTRY[state.current_step]
            step.render(st, state)
        else:
            st.warning("Step UI unavailable. Use the chat below for guidance.")

        st.markdown("---")

        # Shared chat
        user_text = chat_card(st, state)
        if user_text:
            # append user message
            state.messages.append({"role": "user", "content": user_text})

            # call model (or graceful fallback)
            if _ai_ok:
                try:
                    from google.genai import types
                    parts = [
                        types.Content(
                            role=("user" if m["role"] == "user" else "model"),
                            parts=[types.Part(text=m["content"])],
                        )
                        for m in state.messages[-10:]
                    ]
                    resp = chat_once(parts)
                    text = getattr(resp, "text", None) or "I’m here to help."
                except Exception as e:
                    text = f"Model error: {e}"
            else:
                # echo fallback
                text = "AI is not configured right now. Echo: " + user_text

            state.messages.append({"role": "assistant", "content": text})
            st.rerun()

try:
    resp = chat_once(parts)
    text = getattr(resp, "text", None) or "I’m here to help."
except Exception as e:
    text = f"Model error: {e}"

if __name__ == "__main__":
    main()
