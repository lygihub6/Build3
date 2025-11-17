
from typing import Dict, Any

import streamlit as st

from steps.base import Step
from services.ai import call_gemini_for_module


class FeedbackStep(Step):
    def __init__(self):
        super().__init__(id="feedback", title="Meta-Feedback", icon="🧠")

    def render(self, session: Dict[str, Any]):
        self.show_header()
        st.markdown(
            "Use this space to reflect on your **learning habits** and how you are using this app."
        )

        msg = st.text_area(
            "What is working or not working in how you study or use this tool?",
            key="feedback_input",
            height=150,
        )

        if st.button("Get feedback", key="feedback_button") and msg.strip():
            with st.spinner("Thinking with you about your habits..."):
                reply = call_gemini_for_module("feedback", msg, session)
            st.session_state["ai_responses"]["feedback"] = reply

        if st.session_state["ai_responses"].get("feedback"):
            st.markdown("###### AI feedback")
            st.markdown(st.session_state["ai_responses"]["feedback"])
