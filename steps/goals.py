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
        st.subheader("🎯 Goal Setting")
        st.markdown(
            "Focus on **mastery goals** – goals about understanding, skills, and growth, not just grades."
        )

        # Tip about being specific
        st.info(
            'Tip: Be specific with your goals. Instead of **"study math,"** '
            'try **"review 10 practice problems on quadratic equations."**'
        )

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
            # Card-based goal type selector
            st.markdown(
                """
                <style>
                /* Card-based goal selector */
                .goal-type-cards-container {
                    margin-bottom: 1rem;
                }
                
                .goal-type-cards-label {
                    display: block;
                    font-weight: 500;
                    color: #1f2937;
                    margin-bottom: 0.75rem;
                    font-size: 0.875rem;
                }
                
                .goal-type-cards {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 0.75rem;
                    margin-bottom: 1rem;
                }
                
                .goal-card {
                    padding: 1rem;
                    border: 2px solid #e5e7eb;
                    border-radius: 0.5rem;
                    cursor: pointer;
                    transition: all 0.2s;
                    background: white;
                    position: relative;
                }
                
                .goal-card:hover {
                    border-color: #cbd5e1;
                    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                
                .goal-card.selected {
                    border-color: #8b5cf6;
                    background: #f3f0ff;
                }
                
                .goal-card.performance.selected {
                    border-color: #ec4899;
                    background: #fdf2f8;
                }
                
                .goal-card-header {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    margin-bottom: 0.5rem;
                }
                
                .goal-card-icon {
                    width: 20px;
                    height: 20px;
                    border-radius: 0.375rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.75rem;
                }
                
                .goal-card.mastery .goal-card-icon {
                    background: #8b5cf6;
                }
                
                .goal-card.performance .goal-card-icon {
                    background: #ec4899;
                }
                
                .goal-card-title {
                    font-weight: 600;
                    color: #1f2937;
                    font-size: 0.875rem;
                }
                
                .goal-card-description {
                    font-size: 0.75rem;
                    color: #6b7280;
                    line-height: 1.4;
                }
                
                /* Hide the default radio buttons */
                .stRadio {
                    display: none !important;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            
            # Hidden radio buttons for state management
            goal_type_radio = st.radio(
                "Which best matches your main goal for this task?",
                options=[
                    "mastery (understand deeply)",
                    "performance (get a grade/score)",
                ],
                index=0 if session.get("goal_type", "mastery") == "mastery" else 1,
                key="goal_type_radio",
            )
            
            # Determine selected state
            current_goal = "mastery" if goal_type_radio.startswith("mastery") else "performance"
            mastery_selected = "selected" if current_goal == "mastery" else ""
            performance_selected = "selected" if current_goal == "performance" else ""
            
            # Visual card selector
            st.markdown(
                f"""
                <div class="goal-type-cards-container">
                    <label class="goal-type-cards-label">Which best matches your main goal for this task?</label>
                    <div class="goal-type-cards">
                        <div class="goal-card mastery {mastery_selected}" onclick="
                            const radios = parent.document.querySelectorAll('input[type=radio]');
                            if (radios[0]) radios[0].click();
                        ">
                            <div class="goal-card-header">
                                <div class="goal-card-icon">🌟</div>
                                <div class="goal-card-title">Mastery</div>
                            </div>
                            <div class="goal-card-description">Understand deeply</div>
                        </div>
                        <div class="goal-card performance {performance_selected}" onclick="
                            const radios = parent.document.querySelectorAll('input[type=radio]');
                            if (radios[1]) radios[1].click();
                        ">
                            <div class="goal-card-header">
                                <div class="goal-card-icon">🏆</div>
                                <div class="goal-card-title">Performance</div>
                            </div>
                            <div class="goal-card-description">Get a grade/score</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
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

            # Keep a local “last saved goal” so it shows immediately this run
            st.session_state["last_saved_goal"] = goal_payload

            st.success("Goal saved. Next, you can analyze the task or pick strategies.")

        # -------- Show saved goal summary --------
        saved_goal = st.session_state.get("last_saved_goal") or session.get("goal", {})

        if saved_goal and (
            saved_goal.get("task_name")
            or saved_goal.get("goal_text")
            or saved_goal.get("goal_description")
        ):
            st.markdown("##### Your saved goal")
            with st.container():
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

        # -------- Divider + AI helper --------
        st.markdown("---")
        st.markdown("##### Ask AI to refine your goal")

        user_msg = st.text_area(
            "Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.",
            key="goal_ai_input",
            height=100,
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
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])


        # Display AI response
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("##### 🤖 AI Suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])

