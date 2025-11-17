"""
Task analysis step implementation.

In this step, students unpack their assignments by listing the key
requirements and grading criteria, breaking down the work into smaller
pieces, identifying what they already know, what they need to learn,
and anticipating potential obstacles. A call to the Gemini API
provides feedback on their breakdown and may suggest improvements.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class TaskAnalysisStep(BaseStep):
    """Task analysis SRL step."""

    id = "task"
    label = "Task Analysis"
    emoji = "🔍"
    description = "Break the task into clear, manageable pieces."

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("🔍 Task Analysis")
        if not session.get("task_name"):
            st.info("Set a task and goal in **Goal Setting** first, then come back here.")
            return

        # Display current task context for reference
        st.markdown(
            f"**Current task:** {session['task_name']}  \n"
            f"**Goal type:** {session.get('goal_type', 'mastery').title()}  ｜  "
            f"**Task type:** {session.get('task_type', 'not specified')}"
        )

        # ---------------- Editable fields ----------------
        # Requirements
        requirements = st.text_area(
            "What are the key requirements or rubric criteria?",
            value=session.get("requirements", ""),
            key="task_requirements",
            height=120,
        )
        # Subtasks
        subtasks = st.text_area(
            "Break your task into smaller subtasks (one per line).",
            value=session.get("subtasks", ""),
            key="task_subtasks",
            height=120,
            placeholder="e.g.,\nFind 5 credible sources\nCreate an outline\nDraft introduction\n...",
        )
        # Prior knowledge and gaps
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
        # Challenges and contingency
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

        # ---------------- Save button ----------------
        if st.button("Save task analysis", key="save_task_analysis"):
            payload = {
                "requirements": requirements.strip(),
                "subtasks": subtasks.strip(),
                "prior_knowledge": prior_knowledge.strip(),
                "knowledge_gaps": knowledge_gaps.strip(),
                "anticipated_challenges": challenges.strip(),
                "contingency_plan": contingency.strip(),
            }
            update_current_session(payload)
            # Keep a copy so the summary shows immediately this run
            st.session_state["last_task_analysis"] = payload
            st.success("Task analysis saved ✅")

        # ---------------- Saved analysis summary card ----------------
        saved = st.session_state.get("last_task_analysis") or {
            "requirements": session.get("requirements", ""),
            "subtasks": session.get("subtasks", ""),
            "prior_knowledge": session.get("prior_knowledge", ""),
            "knowledge_gaps": session.get("knowledge_gaps", ""),
            "anticipated_challenges": session.get("anticipated_challenges", ""),
            "contingency_plan": session.get("contingency_plan", ""),
        }

        if any(saved.values()):
            st.markdown("##### Your saved task analysis")
            with st.container():
                if saved.get("requirements"):
                    st.markdown("**Key requirements / rubric criteria**")
                    st.markdown(f"> {saved['requirements']}")
                if saved.get("subtasks"):
                    st.markdown("**Subtasks**")
                    lines = [l.strip() for l in saved["subtasks"].splitlines() if l.strip()]
                    if lines:
                        for l in lines:
                            st.markdown(f"- {l}")
                if saved.get("prior_knowledge") or saved.get("knowledge_gaps"):
                    cols = st.columns(2)
                    with cols[0]:
                        if saved.get("prior_knowledge"):
                            st.markdown("**What you already know**")
                            st.markdown(f"> {saved['prior_knowledge']}")
                    with cols[1]:
                        if saved.get("knowledge_gaps"):
                            st.markdown("**What you need to review / learn**")
                            st.markdown(f"> {saved['knowledge_gaps']}")
                if saved.get("anticipated_challenges"):
                    st.markdown("**Anticipated challenges**")
                    st.markdown(f"> {saved['anticipated_challenges']}")
                if saved.get("contingency_plan"):
                    st.markdown("**Plan B (if challenges happen)**")
                    st.markdown(f"> {saved['contingency_plan']}")

        # ---------------- AI helper ----------------
        st.markdown("---")
        st.markdown("##### Ask AI to check your breakdown")
        msg = st.text_area(
            "Paste your assignment instructions or your notes, and the assistant can suggest a clearer breakdown.",
            key="task_ai_input",
            height=120,
        )
        if st.button("🔍 Improve my breakdown", key="task_ai_button") and msg.strip():
            with st.spinner("Analyzing your task..."):
                reply = call_gemini_for_module(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        # Show AI reply
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])

