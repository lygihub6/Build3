from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session
from services.ai import call_gemini_for_module


class StrategiesStep(Step):
    def __init__(self):
        super().__init__(id="strategies", title="Learning Strategies", icon="💡")

    def render(self, session: Dict[str, Any]):
        self.show_header()
        st.markdown(
            "Select strategies you'd like to try for this task. Start with a few and actually use them."
        )

        strategy_options = [
            "Elaborative interrogation (ask why/how questions)",
            "Self-explanation (teach it aloud or in writing)",
            "Spaced practice (short sessions over days)",
            "Practice testing (quiz yourself)",
            "Concept mapping / diagrams",
            "Worked examples then fading",
            "Interleaving different problem types",
        ]

        chosen = st.multiselect(
            "Which strategies do you plan to use?",
            options=strategy_options,
            default=[s for s in strategy_options if s in session.get("chosen_strategies", [])],
            key="strategies_multiselect",
        )

        plan = st.text_area(
            "How will you use these strategies in this task?",
            value=session.get("session_plan", ""),
            key="strategies_plan",
            height=120,
            placeholder=(
                "Example: On Monday I will skim all articles, then on Tuesday I will do self-explanation "
                "notes for two of them..."
            ),
        )

        if st.button("Save strategy plan", key="save_strategies"):
            update_current_session({"chosen_strategies": chosen, "session_plan": plan.strip()})
            st.success("Strategy plan saved ✅")

        st.markdown("---")
        st.markdown("##### Ask AI for strategy ideas")

        msg = st.text_area(
            "Describe your situation (time available, task type, how you like to study), "
            "and the assistant will suggest strategies.",
            key="strategies_ai_input",
            height=120,
        )

        if st.button("✨ Suggest strategies", key="strategies_ai_button") and msg.strip():
            with st.spinner("Brainstorming strategies with you..."):
                reply = call_gemini_for_module("strategies", msg, session)
            st.session_state["ai_responses"]["strategies"] = reply

        if st.session_state["ai_responses"].get("strategies"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["strategies"])
