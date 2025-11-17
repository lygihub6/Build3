from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session
from services.ai import call_gemini_for_module


class GoalsStep(Step):
    def __init__(self):
        super().__init__(id="goals", title="Goal Setting", icon="🎯")

    def render(self, session: Dict[str, Any]):
        self.show_header()
        st.markdown(
            "Focus on **mastery goals** – goals about understanding, skills, and growth, not just grades."
        )

        col1, col2 = st.columns(2)

        with col1:
            task_name = st.text_input(
                "What task or assignment are you working on?",
                value=session.get("task_name", ""),
                key="goal_task_name",
                placeholder="e.g., Research paper on climate change",
            )

            task_type_options = [
                "",
                "Research paper",
                "Problem-solving assignment",
                "Reading / article",
                "Exam preparation",
                "Project",
                "Presentation",
                "Other",
            ]
            current_type = session.get("task_type", "")
            idx = task_type_options.index(current_type) if current_type in task_type_options else 0

            task_type = st.selectbox(
                "What type of task is this?",
                task_type_options,
                index=idx,
                key="goal_task_type",
            )

            deadline = st.date_input(
                "Target completion date (optional)",
                value=None,
                key="goal_deadline",
            )

        with col2:
            goal_type = st.radio(
                "Which best matches your main goal for this task?",
                options=["mastery (understand deeply)", "performance (get a grade/score)"],
                index=0 if session.get("goal_type", "mastery") == "mastery" else 1,
                key="goal_type_radio",
            )

            goal_description = st.text_area(
                "Describe your **mastery goal** in your own words",
                value=session.get("goal_description", ""),
                key="goal_description",
                placeholder="What do you want to understand or be able to do after this task?",
                height=120,
            )

        if st.button("Save goal", key="save_goal_main"):
            update_current_session(
                {
                    "task_name": task_name.strip(),
                    "task_type": task_type.strip(),
                    "goal_type": "mastery"
                    if goal_type.startswith("mastery")
                    else "performance",
                    "goal_description": goal_description.strip(),
                    "deadline": str(deadline) if deadline else "",
                }
            )
            st.success("Goal saved.")

        st.markdown("---")
        st.markdown("##### Ask AI to refine your goal")

        user_msg = st.text_area(
            "Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.",
            key="goal_ai_input",
            height=100,
        )

        if st.button("✨ Improve my goal", key="goal_ai_button") and user_msg.strip():
            with st.spinner("Thinking about your goal..."):
                reply = call_gemini_for_module("goal", user_msg, session)
            st.session_state["ai_responses"]["goals"] = reply

        if st.session_state["ai_responses"].get("goals"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["goals"])
