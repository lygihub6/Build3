# steps/save_session.py
import streamlit as st
from steps.base import StepModule
from state import SRLState
from datetime import datetime

class SaveStep(StepModule):
    key, label, icon = "save", "Save for Next Time", "💾"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Save this Session")
        note = st.text_area("Add a short note or next-step reminder (optional)")
        if st.button("Save Now"):
            payload = {
                "timestamp": datetime.now().isoformat(),
                "goals": state.learning_goals,
                "task": state.task_info,
                "strategies": state.strategies,
                "time_plan": state.time_plan,
                "resources": state.resources,
                "reflections": state.reflections,
                "messages": state.messages[-10:],  # last 10
                "note": note.strip(),
            }
            state.saved_sessions.append(payload)
            st.success("Session saved. You can load it later from the sidebar.")
