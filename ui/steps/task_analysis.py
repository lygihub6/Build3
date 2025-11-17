
from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session
from services.ai import call_gemini_for_module


class TaskAnalysisStep(Step):
    def __init__(self):
        super().__init__(id="task_analysis", title="Task Analysis", icon="🔍")

    def render(self, session: Dict[str, Any]):
        self.show_header()

        if not session.get("task_name"):
            st.info("Set a task and goal in **Goal Setting** first, then come back here.")

        requirements = st.text_area(
            "What are the key requirements or rubric criteria?",
            value=session.get("requirements", ""),
            key="task_requirements",
            height=120,
        )

        subtasks = st.text_area(
            "Break your task into smaller subtasks (one per line).",
            value=session.get("subtasks", ""),
            key="task_subtasks",
            height=120,
            placeholder="e.g.,\nFind 5 credible sources\nCreate an outline\nDraft introduction\n...",
        )

        col1, col2 = st.columns(2)
        with col1:
            prior_knowledge = st.text_area(
                "What do you already know that might help?",
                value=session.get("prior_knowledge", ""),
                key="task_prior",
                height=100,
            )
        with col2:
            knowledge_gaps = st.text_area(
                "What do you need to review or learn?",
                value=session.get("knowledge_gaps", ""),
                key="task_gaps",
                height=100,
            )

        challenges = st.text_area(
            "What challenges do you anticipate?",
            value=session.get("anticipated_challenges", ""),
            key="task_challenges",
            height=100,
        )

        contingency = st.text_area(
            "If those challenges happen, what is your plan B?",
            value=session.get("contingency_plan", ""),
            key="task_contingency",
            height=100,
        )

        if st.button("Save task analysis", key="save_task_analysis"):
            update_current_session(
                {
                    "requirements": requirements.strip(),
                    "subtasks": subtasks.strip(),
                    "prior_knowledge": prior_knowledge.strip(),
                    "knowledge_gaps": knowledge_gaps.strip(),
                    "anticipated_challenges": challenges.strip(),
                    "contingency_plan": contingency.strip(),
                }
            )
            st.success("Task analysis saved ✅")

        st.markdown("---")
        st.markdown("##### Ask AI to check your breakdown")

        msg = st.text_area(
            "Paste your assignment instructions or your notes, and the assistant can suggest a clearer breakdown.",
            key="task_ai_input",
            height=120,
        )

        if st.button("🔍 Improve my breakdown", key="task_ai_button") and msg.strip():
            with st.spinner("Analyzing your task..."):
                reply = call_gemini_for_module("task", msg, session)
            st.session_state["ai_responses"]["task_analysis"] = reply

        if st.session_state["ai_responses"].get("task_analysis"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["task_analysis"])
