# steps/task_analysis.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

class TaskAnalysisStep(StepModule):
    key, label, icon = "task_analysis", "Task Analysis", "📋"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Analyze the Task")
        prior = st.text_area("What do you already know?")
        reqs = st.text_area("What are the task requirements?")
        gaps = st.text_area("What is unclear?")
        if st.button("Save Task Analysis"):
            state.task_info = "\n".join([
                f"Prior: {prior.strip()}",
                f"Requirements: {reqs.strip()}",
                f"Gaps: {gaps.strip()}",
            ])
            st.success("Saved.")
            st.rerun()
