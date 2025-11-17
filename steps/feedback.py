"""
Feedback step implementation.

This optional module allows students to request high‑level feedback on
their overall study habits or their use of the app. It exposes a
single text input where the student can describe their situation or
concerns and then calls the Gemini API to generate supportive,
constructive feedback.
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict

from services.ai import call_gemini_for_module
from .base import BaseStep


class FeedbackStep(BaseStep):
    """Feedback SRL step."""

    id = "feedback"
    label = "Feedback"
    emoji = "📝"
    description = "High‑level feedback on your study habits and app use."

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("📝 Feedback")
        st.markdown(
            "This section lets you ask for general feedback on your study habits, use of strategies, or anything else related to learning."
        )
        msg = st.text_area(
            "Describe any patterns you're noticing or questions you have about your study habits.",
            key="feedback_input",
            height=150,
        )
        if st.button("💬 Get feedback", key="feedback_button") and msg.strip():
            with st.spinner("Gathering feedback..."):
                reply = call_gemini_for_module(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])