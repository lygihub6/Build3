"""
Time planning step implementation.

This module allows students to track the time spent on their current
task using a simple timer, set estimates for upcoming study sessions,
and record a break schedule. It also provides a summary of recent
planned sessions and an AI‑powered assistant to help integrate the
task into a weekly schedule. The underlying timer logic is handled by
the ``state`` module.
"""

from __future__ import annotations

import time
import streamlit as st
from typing import Any, Dict

import state
from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class TimePlanStep(BaseStep):
    """Time planning SRL step."""

    id = "time"
    label = "Time Management"
    emoji = "⏱️"
    description = "Plan and track your study time."

    def render(self, session: Dict[str, Any]) -> None:
        # Synchronize the timer to accumulate elapsed minutes if running
        state.sync_timer_with_session()
        total_minutes = int(session.get("total_time_minutes", 0))
        st.subheader("⏱️ Time Management")
        st.markdown(
            f"**Logged study time for this task:** `{state.format_time_from_minutes(total_minutes)}`"
        )
        # Timer controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Start / continue timer", key="timer_start", use_container_width=True):
                state.start_timer()
            if st.button("⏸️ Pause timer", key="timer_pause", use_container_width=True):
                state.pause_timer()
            if st.button("⏹️ Reset total logged time", key="timer_reset", use_container_width=True):
                state.reset_timer()
        with col2:
            est_minutes = st.number_input(
                "For your **next** study session, how many minutes do you plan to work?",
                min_value=5,
                max_value=240,
                step=5,
                value=45,
                key="time_estimate",
            )
            break_pattern = st.selectbox(
                "Break schedule",
                [
                    "Pomodoro (25 min work, 5 min break)",
                    "50-10 (50 work, 10 break)",
                    "Long focus (90 min work, 15 min break)",
                    "Custom / flexible",
                ],
                key="time_break_pattern",
            )
        # Save planned session
        if st.button("Save time plan", key="save_time_plan"):
            recent = list(session.get("recent_sessions", []))
            recent.insert(
                0,
                {
                    "estimated_minutes": int(est_minutes),
                    "break_pattern": break_pattern,
                    "created_at": time.time(),
                },
            )
            # Keep only the last 10 entries
            recent = recent[:10]
            update_current_session({"recent_sessions": recent})
            st.success("Time plan saved ✅")
        # Show recent planned sessions
        if session.get("recent_sessions"):
            st.markdown("##### Recent planned sessions")
            for s_item in session["recent_sessions"]:
                ts = time.strftime("%b %d, %Y", time.localtime(s_item.get("created_at", time.time())))
                st.markdown(
                    f"- `{ts}` – planned {s_item.get('estimated_minutes', 0)} min ｜ {s_item.get('break_pattern', '')}"
                )
        st.markdown("---")
        st.markdown("##### Ask AI to adjust your schedule")
        msg = st.text_area(
            "Explain your weekly schedule and constraints, and the assistant can help you fit this task in realistically.",
            key="time_ai_input",
            height=120,
        )
        if st.button("🗓️ Help me plan my week", key="time_ai_button") and msg.strip():
            with st.spinner("Planning around your schedule..."):
                reply = call_gemini_for_module(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])