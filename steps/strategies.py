"""
Learning strategies step implementation.

In this step, students choose evidence‑based learning strategies that fit
their task and preferences. A multiselect widget allows them to pick
from a curated list of common strategies. They can also describe how
they plan to implement these strategies for the current task. An AI
assistant can suggest additional strategies based on the student’s
input.
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict, List

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class StrategiesStep(BaseStep):
    """Learning strategies SRL step."""

    id = "strategies"
    label = "Learning Strategies"
    emoji = "💡"
    description = "Choose evidence‑based strategies for this task."

    # List of strategy options presented to the student
    STRATEGY_OPTIONS: List[str] = [
        "Elaborative interrogation (ask why/how questions)",
        "Self‑explanation (teach it aloud or in writing)",
        "Spaced practice (short sessions over days)",
        "Practice testing (quiz yourself)",
        "Concept mapping / diagrams",
        "Worked examples then fading",
        "Interleaving different problem types",
    ]

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("💡 Learning Strategies")
        st.markdown(
            "Select strategies you'd like to try for this task. Start with a few and actually use them."
        )
        # Multiselect for strategies
        chosen = st.multiselect(
            "Which strategies do you plan to use?",
            options=self.STRATEGY_OPTIONS,
            default=[s for s in self.STRATEGY_OPTIONS if s in session.get("chosen_strategies", [])],
            key="strategies_multiselect",
        )
        # Plan text area
        plan = st.text_area(
            "How will you use these strategies in this task?",
            value=session.get("session_plan", ""),
            key="strategies_plan",
            height=120,
            placeholder=(
                "Example: On Monday I will skim all articles, then on Tuesday I will do self‑explanation "
                "notes for two of them..."
            ),
        )
        if st.button("Save strategy plan", key="save_strategies"):
            update_current_session(
                {
                    "chosen_strategies": chosen,
                    "session_plan": plan.strip(),
                }
            )
            st.success("Strategy plan saved ✅")
        st.markdown("---")
        st.markdown("##### Ask AI for strategy ideas")
        msg = st.text_area(
            "Describe your situation (time available, task type, how you like to study), and the assistant will suggest strategies.",
            key="strategies_ai_input",
            height=120,
        )
        if st.button("✨ Suggest strategies", key="strategies_ai_button") and msg.strip():
            with st.spinner("Brainstorming strategies with you..."):
                reply = call_gemini_for_module(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])