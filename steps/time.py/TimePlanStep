"""
Time planning step implementation.

This module allows students to track the time spent on their current
task using a simple timer, set estimates for upcoming study sessions,
and record a break schedule. It also provides a summary of recent
planned sessions and an AI-powered assistant to help integrate the
task into a weekly schedule.
"""

from __future__ import annotations

import time
from typing import Any, Dict

import streamlit as st

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


def _format_hhmmss(total_seconds: int) -> str:
    """Format seconds as HH:MM:SS."""
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class TimePlanStep(BaseStep):
    """Time planning SRL step."""

    id = "time"
    label = "Time Management"
    emoji = "⏱️"
    description = "Plan and track your study time."

    def render(self, session: Dict[str, Any]) -> None:
        # ---------- Initialize timer state (before any widgets) ----------
        # Store timer in seconds in Streamlit session_state
        if "timer_total_seconds" not in st.session_state:
            # If we already have minutes stored in the SRL session, pull them in
            minutes_from_session = float(session.get("total_time_minutes", 0))
            st.session_state["timer_total_seconds"] = int(minutes_from_session * 60)

        if "timer_running" not in st.session_state:
            st.session_state["timer_running"] = False

        if "timer_last_tick" not in st.session_state:
            st.session_state["timer_last_tick"] = time.time()

        # ---------- Update timer if it's currently running ----------
        now = time.time()
        if st.session_state["timer_running"]:
            elapsed = now - st.session_state["timer_last_tick"]
            if elapsed > 0:
                st.session_state["timer_total_seconds"] += int(elapsed)
                st.session_state["timer_last_tick"] = now

                # Persist updated minutes into the SRL session
                total_minutes = st.session_state["timer_total_seconds"] / 60.0
                update_current_session({"total_time_minutes": total_minutes})

        total_seconds = int(st.session_state["timer_total_seconds"])
        time_display = _format_hhmmss(total_seconds)

        # ---------- UI: header + current logged time ----------
        st.subheader("⏱️ Time Management")
        st.markdown(
            f"**Logged study time for this task:** "
            f"`{time_display}`"
        )

        # ---------- Timer controls + planning controls ----------
        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶️ Start / continue timer", key="timer_start", use_container_width=True):
                # Start or resume: mark running and reset last_tick
                st.session_state["timer_running"] = True
                st.session_state["timer_last_tick"] = time.time()

            if st.button("⏸️ Pause timer", key="timer_pause", use_container_width=True):
                # Pause: do one more update and then freeze
                now = time.time()
                if st.session_state["timer_running"]:
                    elapsed = now - st.session_state["timer_last_tick"]
                    if elapsed > 0:
                        st.session_state["timer_total_seconds"] += int(elapsed)
                    st.session_state["timer_running"] = False
                    st.session_state["timer_last_tick"] = now
                    total_minutes = st.session_state["timer_total_seconds"] / 60.0
                    update_current_session({"total_time_minutes": total_minutes})

            if st.button("⏹️ Reset total logged time", key="timer_reset", use_container_width=True):
                st.session_state["timer_running"] = False
                st.session_state["timer_total_seconds"] = 0
                st.session_state["timer_last_tick"] = time.time()
                update_current_session({"total_time_minutes": 0})
                st.success("Timer reset.")

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

        # ---------- Save planned session ----------
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

        # ---------- Show recent planned sessions ----------
        if session.get("recent_sessions"):
            st.markdown("##### Recent planned sessions")
            for s_item in session["recent_sessions"]:
                ts = time.strftime(
                    "%b %d, %Y",
                    time.localtime(s_item.get("created_at", time.time())),
                )
                st.markdown(
                    f"- `{ts}` – planned {s_item.get('estimated_minutes', 0)} min ｜ "
                    f"{s_item.get('break_pattern', '')}"
                )

        st.markdown("---")

        # ---------- AI helper ----------
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

        # ---------- Auto-refresh while timer is running ----------
        if st.session_state["timer_running"]:
            # Simple 1-second loop so the display updates live
            time.sleep(1)
            st.experimental_rerun()
