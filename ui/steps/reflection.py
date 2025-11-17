
from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session
from services.ai import call_gemini_for_module


class ReflectionStep(Step):
    def __init__(self):
        super().__init__(id="reflection", title="Reflection", icon="✨")

    def render(self, session: Dict[str, Any]):
        self.show_header()
        st.markdown(
            "Reflection helps you close the loop: connect what happened to what you want to change next time."
        )

        refs = session.get(
            "reflections",
            {"goal": "", "strategies": "", "time": "", "growth": ""},
        )

        goal_ref = st.text_area(
            "1. Goal achievement – What did you actually learn or understand? Did you reach your mastery goal?",
            value=refs.get("goal", ""),
            key="refl_goal",
            height=120,
        )

        strat_ref = st.text_area(
            "2. Strategies – Which strategies helped most? Which did you not use or found unhelpful?",
            value=refs.get("strategies", ""),
            key="refl_strategies",
            height=120,
        )

        time_ref = st.text_area(
            "3. Time & focus – How well did you stick to your plan? What affected your focus?",
            value=refs.get("time", ""),
            key="refl_time",
            height=120,
        )

        growth_ref = st.text_area(
            "4. Next steps – What will you do differently for the next similar task?",
            value=refs.get("growth", ""),
            key="refl_growth",
            height=120,
        )

        if st.button("Save reflection", key="save_reflection"):
            update_current_session(
                {
                    "reflections": {
                        "goal": goal_ref.strip(),
                        "strategies": strat_ref.strip(),
                        "time": time_ref.strip(),
                        "growth": growth_ref.strip(),
                    }
                }
            )
            st.success("Reflection saved 🌱")

        st.markdown("---")
        st.markdown("##### Ask AI to deepen your reflection")

        msg = st.text_area(
            "Paste a short summary of what happened, and the assistant will highlight patterns and suggest 1–2 next steps.",
            key="reflection_ai_input",
            height=150,
        )

        if st.button("🪞 Help me reflect", key="reflection_ai_button") and msg.strip():
            with st.spinner("Thinking with you about this experience..."):
                reply = call_gemini_for_module("reflection", msg, session)
            st.session_state["ai_responses"]["reflection"] = reply

        if st.session_state["ai_responses"].get("reflection"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["reflection"])
