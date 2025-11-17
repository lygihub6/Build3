"""
Goal setting step implementation.

This module defines the UI for the goal setting stage of the SRL
cycle. Students clarify the task they are working on, select the type
of task, specify whether their main goal is mastery or performance, and
describe their goal in detail. They can also set a tentative deadline.
An embedded call to the Gemini API offers feedback and suggestions
for refining the goal.
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class GoalsStep(BaseStep):
    """Goal setting SRL step."""

    id = "goal"
    label = "Goal Setting"
    emoji = "🎯"
    description = "Define mastery‑oriented goals for your current task."

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("🎯 Goal Setting")
        st.markdown(
            "Focus on **mastery goals** – goals about understanding, skills, and growth, not just grades."
        )

        col1, col2 = st.columns(2)
        # First column: task name, type, deadline
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
                "Problem‑solving assignment",
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
            # Date input returns a datetime.date or None
            deadline_date = st.date_input(
                "Target completion date (optional)",
                key="goal_deadline",
                value=None,
                help="You can leave this as default if you're not sure.",
            )
        # Second column: goal type and description
        with col2:
            goal_type_radio = st.radio(
                "Which best matches your main goal for this task?",
                options=["mastery (understand deeply)", "performance (get a grade/score)"],
                index=0 if session.get("goal_type", "mastery") == "mastery" else 1,
                key="goal_type_radio",
            )
            goal_description = st.text_area(
                "Describe your **mastery goal** in your own words",
                value=session.get("goal_description", ""),
                key="goal_description",
                placeholder=(
                    "What do you want to understand or be able to do after this task?"
                ),
                height=120,
            )
        # Save button
        if st.button("Save goal", key="save_goal_main"):
            update_current_session(
                {
                    "task_name": task_name.strip(),
                    "task_type": task_type.strip(),
                    "goal_type": "mastery"
                    if goal_type_radio.startswith("mastery")
                    else "performance",
                    "goal_description": goal_description.strip(),
                    "deadline": str(deadline_date) if deadline_date else "",
                }
            )
            st.success("Goal saved. Next, you can analyze the task or pick strategies.")
        # Divider
        st.markdown("---")
        # AI suggestion area
        st.markdown("##### Ask AI to refine your goal")
        user_msg = st.text_area(
            "Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.",
            key="goal_ai_input",
            height=100,
        )
        if st.button("✨ Improve my goal", key="goal_ai_button") and user_msg.strip():
            with st.spinner("Thinking about your goal..."):
                reply = call_gemini_for_module(self.id, user_msg, session)
            # Cache and display the response
            st.session_state.setdefault("ai_responses", {})[self.id] = reply
        # Display last AI response if available
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])