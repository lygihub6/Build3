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
        # Custom CSS matching the HTML mockup
        st.markdown(
            """
            <style>
            /* Module header styling */
            .module-header {
                margin-bottom: 1.5rem;
            }
            
            .module-header h2 {
                font-size: 1.5rem;
                font-weight: 700;
                color: #1f2937;
                margin-bottom: 0.25rem;
            }
            
            .module-header-subtitle {
                font-size: 0.95rem;
                color: #6b7280;
            }
            
            /* Alert box styling - matching HTML mockup */
            .alert-info {
                padding: 1rem 1.25rem;
                border-radius: 0.5rem;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                background-color: #dbeafe;
                color: #1e3a8a;
            }
            
            .alert-icon {
                font-size: 1.25rem;
                flex-shrink: 0;
            }
            
            .alert-content {
                flex: 1;
            }
            
            .alert-title {
                font-weight: 600;
                margin-bottom: 0.25rem;
                font-size: 0.95rem;
            }
            
            .alert-message {
                font-size: 0.875rem;
                line-height: 1.5;
            }
            
            /* Form styling */
            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stDateInput > label {
                font-weight: 500 !important;
                color: #1f2937 !important;
                margin-bottom: 0.5rem !important;
                font-size: 0.875rem !important;
            }
            
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select,
            .stDateInput > div > div > input {
                border: 1px solid #e5e7eb !important;
                border-radius: 0.5rem !important;
                padding: 1rem !important;
                font-size: 1rem !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stSelectbox > div > div > select:focus {
                border-color: #2563eb !important;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
            }
            
            /* Form hints */
            .form-hint {
                font-size: 0.75rem;
                color: #9ca3af;
                margin-top: 0.25rem;
                font-style: italic;
            }
            
            /* Goal type selector - card-based like HTML mockup */
            .goal-type-selector {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .goal-type-card {
                padding: 1.25rem;
                border: 2px solid #e5e7eb;
                border-radius: 0.75rem;
                cursor: pointer;
                transition: all 0.2s;
                background: white;
            }
            
            .goal-type-card:hover {
                border-color: #cbd5e1;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            
            .goal-type-card.selected {
                border-color: #8b5cf6;
                background: #ede9fe;
            }
            
            .goal-type-card.performance.selected {
                border-color: #ec4899;
                background: #fce7f3;
            }
            
            .goal-type-header {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 0.5rem;
            }
            
            .goal-type-icon {
                width: 24px;
                height: 24px;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.875rem;
            }
            
            .goal-type-card.mastery .goal-type-icon {
                background: #8b5cf6;
                color: white;
            }
            
            .goal-type-card.performance .goal-type-icon {
                background: #ec4899;
                color: white;
            }
            
            .goal-type-title {
                font-weight: 600;
                color: #1f2937;
            }
            
            .goal-type-description {
                font-size: 0.875rem;
                color: #6b7280;
                line-height: 1.5;
            }
            
            /* Save button styling */
            .stButton > button {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                font-size: 1rem;
                font-weight: 500;
                border-radius: 0.5rem;
                transition: all 0.2s;
            }
            
            .stButton > button:hover {
                background-color: #1e40af;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            /* Saved goal card */
            .saved-goal-card {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 0.5rem;
                padding: 1.25rem;
                margin-top: 1.5rem;
            }
            
            .saved-goal-card h5 {
                color: #1f2937;
                font-size: 1rem;
                margin-bottom: 1rem;
                font-weight: 600;
            }
            
            .saved-goal-card strong {
                color: #374151;
            }
            
            /* Hide default Streamlit radio buttons */
            .stRadio {
                display: none !important;
            }
            
            /* AI section */
            .ai-section {
                margin-top: 2rem;
                padding-top: 2rem;
                border-top: 1px solid #e5e7eb;
            }
            
            .ai-section-title {
                font-size: 1.125rem;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 0.5rem;
            }
            
            .ai-section-description {
                font-size: 0.875rem;
                color: #6b7280;
                margin-bottom: 1rem;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Module header
        st.markdown(
            """
            <div class="module-header">
                <h2>🎯 Goal Setting</h2>
                <p class="module-header-subtitle">Set meaningful goals that drive your learning journey</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Alert box
        st.markdown(
            """
            <div class="alert-info">
                <div class="alert-icon">💡</div>
                <div class="alert-content">
                    <div class="alert-title">Focus on Mastery Goals</div>
                    <div class="alert-message">Mastery goals help you focus on understanding and growth rather than just grades. Research shows they lead to deeper learning and greater persistence.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Form fields
        task_name = st.text_input(
            "What task or assignment are you working on?",
            value=session.get("task_name", ""),
            key="goal_task_name",
            placeholder="e.g., Research paper on climate change",
        )
        st.markdown('<p class="form-hint">Be specific about what you want to accomplish</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
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

        with col2:
            deadline_date = st.date_input(
                "Target completion date",
                key="goal_deadline",
                value=None,
            )

        # Goal type selector with cards
        st.markdown('<label class="stTextInput" style="font-weight: 500; color: #1f2937; margin-bottom: 0.5rem; font-size: 0.875rem; display: block; margin-top: 1rem;">What type of goal do you want to set?</label>', unsafe_allow_html=True)
        
        # Hidden radio buttons for state management
        goal_type_radio = st.radio(
            "Goal type (hidden)",
            options=["mastery", "performance"],
            index=0 if session.get("goal_type", "mastery") == "mastery" else 1,
            key="goal_type_radio",
            label_visibility="collapsed",
        )
        
        # Visual card selector
        current_goal_type = session.get("goal_type", "mastery")
        mastery_selected = "selected" if current_goal_type == "mastery" else ""
        performance_selected = "selected" if current_goal_type == "performance" else ""
        
        st.markdown(
            f"""
            <div class="goal-type-selector">
                <div class="goal-type-card mastery {mastery_selected}" onclick="document.querySelectorAll('input[type=radio]')[0].click()">
                    <div class="goal-type-header">
                        <div class="goal-type-icon">🌟</div>
                        <div class="goal-type-title">Mastery Goal</div>
                    </div>
                    <div class="goal-type-description">Focus on understanding and skill development. Example: "Deeply understand the impact of greenhouse gases on climate systems"</div>
                </div>
                <div class="goal-type-card performance {performance_selected}" onclick="document.querySelectorAll('input[type=radio]')[1].click()">
                    <div class="goal-type-header">
                        <div class="goal-type-icon">🏆</div>
                        <div class="goal-type-title">Performance Goal</div>
                    </div>
                    <div class="goal-type-description">Focus on outcomes and results. Example: "Score at least 90% on the assignment"</div>
                </div>
            </div>
            <p class="form-hint">We recommend setting at least one mastery goal to deepen your learning</p>
            """,
            unsafe_allow_html=True,
        )
        
        # Goal description
        goal_description = st.text_area(
            "Describe your goal in detail",
            value=session.get("goal_description", ""),
            key="goal_description",
            placeholder="What do you want to learn or achieve? Be specific about the knowledge or skills you want to develop...",
            height=120,
        )

        # Save button
        if st.button("Save Goal", key="save_goal_main"):
            goal_type_value = goal_type_radio

            # Try to turn date into ISO string if it exists
            if deadline_date:
                try:
                    deadline_str = deadline_date.isoformat()
                except AttributeError:
                    deadline_str = str(deadline_date)
            else:
                deadline_str = ""

            # Unified goal payload
            goal_payload = {
                "task_name": task_name.strip(),
                "task_type": task_type.strip(),
                "goal_type": goal_type_value,
                "goal_text": goal_description.strip(),
                "deadline": deadline_str,
            }

            update_current_session(
                {
                    "task_name": goal_payload["task_name"],
                    "task_type": goal_payload["task_type"],
                    "goal_type": goal_type_value,
                    "goal_description": goal_payload["goal_text"],
                    "deadline": goal_payload["deadline"],
                    "goal": goal_payload,
                }
            )

            st.session_state["last_saved_goal"] = goal_payload
            st.success("✅ Goal saved successfully! Next, you can analyze the task or pick strategies.")

        # Show saved goal summary
        saved_goal = st.session_state.get("last_saved_goal") or session.get("goal", {})

        if saved_goal and (
            saved_goal.get("task_name")
            or saved_goal.get("goal_text")
            or saved_goal.get("goal_description")
        ):
            st.markdown(
                '<div class="saved-goal-card"><h5>📋 Your Saved Goal</h5>',
                unsafe_allow_html=True,
            )
            
            if saved_goal.get("task_name"):
                st.markdown(f"**Task:** {saved_goal['task_name']}")

            if saved_goal.get("task_type"):
                st.markdown(f"**Task type:** {saved_goal['task_type']}")

            goal_type_value = saved_goal.get("goal_type") or session.get("goal_type")
            if goal_type_value:
                if goal_type_value == "mastery":
                    label = "🌟 Mastery Goal"
                else:
                    label = "🏆 Performance Goal"
                st.markdown(f"**Goal type:** {label}")

            goal_text = saved_goal.get("goal_text") or saved_goal.get("goal_description")
            if goal_text:
                st.markdown("**Goal description:**")
                st.markdown(f"> {goal_text}")

            if saved_goal.get("deadline"):
                st.markdown(f"**Target completion date:** {saved_goal['deadline']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # AI helper section
        st.markdown(
            """
            <div class="ai-section">
                <div class="ai-section-title">💬 Get AI Assistance</div>
                <div class="ai-section-description">Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        user_msg = st.text_area(
            "Your message to AI",
            key="goal_ai_input",
            height=100,
            placeholder="E.g., I want to understand climate change better but don't know where to start...",
        )
        
        if st.button("✨ Get AI Suggestions", key="goal_ai_button") and user_msg.strip():
            with st.spinner("Thinking about your goal..."):
                reply = call_gemini_for_module(self.id, user_msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        # Display AI response
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("##### 🤖 AI Suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])

