# steps/task_analysis.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

class TaskAnalysisStep(StepModule):
    key, label, icon = "task_analysis", "Task Analysis", "📋"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Analyze the Task")

        col1, col2 = st.columns(2)
        with col1:
            prior = st.text_area("1) What do you already know?", value="", height=120)
            reqs  = st.text_area("2) What are the task requirements?", value="", height=120)
        with col2:
            gaps  = st.text_area("3) What concepts/skills are unclear?", value="", height=120)
            criteria = st.text_area("4) What does “good” look like? (rubric/examples)", value="", height=120)

        if st.button("Save Task Analysis"):
            chunks = []
            if prior.strip():   chunks.append(f"Prior knowledge: {prior.strip()}")
            if reqs.strip():    chunks.append(f"Requirements: {reqs.strip()}")
            if gaps.strip():    chunks.append(f"Gaps: {gaps.strip()}")
            if criteria.strip():chunks.append(f"Quality criteria: {criteria.strip()}")
            txt = "\n".join(chunks)
            if txt:
                state.task_info = txt
                st.success("Task analysis saved.")
                st.rerun()

        if state.task_info:
            st.markdown("---")
            st.markdown("**Saved Task Analysis**")
            st.info(state.task_info)
