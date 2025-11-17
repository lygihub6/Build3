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

from typing import Any, Dict

import streamlit as st

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class GoalsStep(BaseStep):
    """Goal setting SRL step."""

    id = "goal"
    label = "Goal Setting"
    emoji = "🎯"
    description = "Define mastery-oriented goals for your current task."

    def render(self, session: Dict[str, Any]) -> None:
        # Custom CSS for the goal setting page
        st.markdown(
            """
            <style>
            /* Goal setting page specific styles */
            .goal-intro {
                font-size: 1.1rem;
                color: #1f2933;
                margin-bottom: 1rem;
                font-weight: 400;
            }
            
            .goal-tip-box {
                background: #e6f3ff;
                border-left: 4px solid #3b82f6;
                padding: 1rem 1.25rem;
                margin: 1.25rem 0;
                border-radius: 0.5rem;
            }
            
            .goal-tip-box p {
                margin: 0;
                font-size: 1rem;
                line-height: 1.6;
                color: #1f2933;
            }
            
            .goal-section {
                background: white;
                padding: 0;
                border-radius: 0.5rem;
                margin-bottom: 1.5rem;
            }
            
            /* Input field styling */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {
                font-size: 1rem !important;
                border-radius: 0.375rem !important;
                border: 1px solid #e2e8f0 !important;
            }
            
            /* Label styling */
            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stDateInput > label,
            .stRadio > label {
                font-size: 1rem !important;
                font-weight: 500 !important;
                color: #1f2933 !important;
                margin-bottom: 0.5rem !important;
            }
            
            /* Radio button styling */
            .stRadio > div {
                gap: 1rem;
            }
            
            .stRadio > div > label > div {
                font-size: 1rem !important;
                padding: 0.5rem 0 !important;
            }
            
            /* Save button styling */
            div[data-testid="column"] > div > button[kind="primary"],
            div[data-testid="column"] > div > button {
                background-color: #f59127;
                color: white;
                border: none;
                padding: 0.625rem 1.5rem;
                font-size: 1rem;
                font-weight: 500;
                border-radius: 0.5rem;
                transition: background-color 0.2s;
            }
            
            div[data-testid="column"] > div > button:hover {
                background-color: #e07e1e;
            }
            
            /* Saved goal summary card */
            .saved-goal-card {
                background: #fef9f3;
                border: 1px solid #f2c9a3;
                border-radius: 0.5rem;
                padding: 1.25rem;
                margin-top: 1.5rem;
            }
            
            .saved-goal-card h5 {
                color: #f59127;
                font-size: 1.125rem;
                margin-bottom: 1rem;
                font-weight: 600;
            }
            
            /* Divider styling */
            hr {
                margin: 2rem 0;
                border: none;
                border-top: 1px solid #e2e8f0;
            }
            
            /* AI section styling */
            .ai-section-header {
                font-size: 1.25rem;
                color: #1f2933;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .ai-section-description {
                font-size: 0.95rem;
                color: #52606d;
                margin-bottom: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        st.subheader("🎯 Goal Setting")
        
        # Introduction text
        st.markdown(
            '<p class="goal-intro">Focus on <strong>mastery goals</strong> – goals about understanding, skills, and growth, not just grades.</p>',
            unsafe_allow_html=True,
        )

        # Tip box
        st.markdown(
            '''
            <div class="goal-tip-box">
                <p><strong>Tip:</strong> Be specific with your goals. Instead of <strong>"study math,"</strong> try <strong>"review 10 practice problems on quadratic equations."</strong></p>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        # Main form section
        st.markdown('<div class="goal-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        # -------- First column: task name, type, deadline --------
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
            idx = (
                task_type_options.index(current_type)
                if current_type in task_type_options
                else 0
            )
            task_type = st.selectbox(
                "What type of task is this?",
                task_type_options,
                index=idx,
                key="goal_task_type",
            )

            # Date input returns a datetime.date or None (depending on version/config)
            deadline_date = st.date_input(
                "Target completion date (optional)",
                key="goal_deadline",
                value=None,
                help="You can leave this as default if you're not sure.",
            )

        # -------- Second column: goal type and description --------
        with col2:
            goal_type_radio = st.radio(
                "Which best matches your main goal for this task?",
                options=[
                    "mastery (understand deeply)",
                    "performance (get a grade/score)",
                ],
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

        st.markdown('</div>', unsafe_allow_html=True)

        # -------- Save button --------
        if st.button("Save goal", key="save_goal_main"):
            goal_type_value = (
                "mastery"
                if goal_type_radio.startswith("mastery")
                else "performance"
            )

            # Try to turn date into ISO string if it exists
            if deadline_date:
                try:
                    deadline_str = deadline_date.isoformat()
                except AttributeError:
                    deadline_str = str(deadline_date)
            else:
                deadline_str = ""

            # Unified goal payload (also stored under session["goal"])
            goal_payload = {
                "task_name": task_name.strip(),
                "task_type": task_type.strip(),
                "goal_type": goal_type_value,
                "goal_text": goal_description.strip(),
                "deadline": deadline_str,
            }

            update_current_session(
                {
                    # top-level fields used elsewhere (e.g., header pills)
                    "task_name": goal_payload["task_name"],
                    "task_type": goal_payload["task_type"],
                    "goal_type": goal_type_value,
                    "goal_description": goal_payload["goal_text"],
                    "deadline": goal_payload["deadline"],
                    # nested goal dict for easy loading/saving
                    "goal": goal_payload,
                }
            )

            # Keep a local "last saved goal" so it shows immediately this run
            st.session_state["last_saved_goal"] = goal_payload

            st.success("Goal saved. Next, you can analyze the task or pick strategies.")

        # -------- Show saved goal summary --------
        saved_goal = st.session_state.get("last_saved_goal") or session.get("goal", {})

        if saved_goal and (
            saved_goal.get("task_name")
            or saved_goal.get("goal_text")
            or saved_goal.get("goal_description")
        ):
            st.markdown(
                '<div class="saved-goal-card"><h5>Your saved goal</h5>',
                unsafe_allow_html=True,
            )
            
            if saved_goal.get("task_name"):
                st.markdown(f"**Task:** {saved_goal['task_name']}")

            if saved_goal.get("task_type"):
                st.markdown(f"**Task type:** {saved_goal['task_type']}")

            goal_type_value = (
                saved_goal.get("goal_type") or session.get("goal_type")
            )
            if goal_type_value:
                if goal_type_value == "mastery":
                    label = "mastery (understand deeply)"
                else:
                    label = "performance (get a grade/score)"
                st.markdown(f"**Goal type:** {label}")

            # Support both new key "goal_text" and older "goal_description"
            goal_text = saved_goal.get("goal_text") or saved_goal.get(
                "goal_description"
            )
            if goal_text:
                st.markdown("**Mastery goal (in your own words):**")
                st.markdown(f"> {goal_text}")

            if saved_goal.get("deadline"):
                st.markdown(
                    f"**Target completion date:** {saved_goal['deadline']}"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

        # -------- Divider + AI helper --------
        st.markdown("---")
        
        st.markdown(
            '<h3 class="ai-section-header">Ask AI to refine your goal</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="ai-section-description">Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.</p>',
            unsafe_allow_html=True,
        )

        user_msg = st.text_area(
            "Your message",
            key="goal_ai_input",
            height=100,
            label_visibility="collapsed",
            placeholder="Describe what you want to achieve...",
        )
        if (
            st.button("✨ Improve my goal", key="goal_ai_button")
            and user_msg.strip()
        ):
            with st.spinner("Thinking about your goal..."):
                reply = call_gemini_for_module(self.id, user_msg, session)
            # Cache and display the response
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        # Display last AI response if available
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("##### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])

