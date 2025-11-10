# steps/feedback.py
import streamlit as st
from steps.base import StepModule
from state import SRLState
from services.ai import chat_once
from google.genai import types

TEMPLATE = (
    "Provide constructive feedback on the student's current plan.\n"
    "Goals: {goals}\nTask: {task}\nStrategies: {strategies}\nTime Plan: {time_plan}\n"
    "Be encouraging, specific, and suggest 2–3 actionable next steps (≤2 minutes each)."
)

class FeedbackStep(StepModule):
    key, label, icon = "feedback", "Feedback", "✅"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Get Feedback")

        if st.button("Ask Sylvia for Feedback"):
            prompt = TEMPLATE.format(
                goals="; ".join(state.learning_goals) or "—",
                task=state.task_info or "—",
                strategies="; ".join(state.strategies) or "—",
                time_plan=state.time_plan or "—",
            )
            history = [types.Content(role="user", parts=[types.Part(text=prompt)])]
            try:
                resp = chat_once(history)
                text = resp.text or "I couldn't generate feedback right now."
                st.session_state.srl.messages.append({"role":"assistant","content":text})
                st.success("Feedback received. See chat below.")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        if state.messages:
            st.markdown("---")
            st.markdown("**Latest assistant message**")
            for m in reversed(state.messages):
                if m["role"] == "assistant":
                    st.info(m["content"])
                    break
