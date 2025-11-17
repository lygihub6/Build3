from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session, sync_timer_with_session, format_time_from_minutes
from services.ai import call_gemini_for_module


class TimePlanStep(Step):
    def __init__(self):
        super().__init__(id="time_plan", title="Time Management", icon="⏱️")

    def render(self, session: Dict[str, Any]):
        self.show_header()

        sync_timer_with_session()
        total_minutes = int(session.get("total_time_minutes", 0))
        st.markdown(
            f"**Logged study time for this task:** `{format_time_from_minutes(total_minutes)}`"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶️ Start / continue timer", key="timer_start", use_container_width=True):
                st.session_state["timer_running"] = True
                st.session_state["timer_start_ts"] = __import__("time").time()

            if st.button("⏸️ Pause timer", key="timer_pause", use_container_width=True):
                st.session_state["timer_running"] = False
                st.session_state["timer_start_ts"] = None

            if st.button("⏹️ Reset total logged time", key="timer_reset", use_container_width=True):
                update_current_session({"total_time_minutes": 0})
                st.session_state["timer_running"] = False
                st.session_state["timer_start_ts"] = None

        with col2:
            est_session_minutes = st.number_input(
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

        if st.button("Save time plan", key="save_time_plan"):
            recent = list(session.get("recent_sessions", []))
            recent.insert(
                0,
                {
                    "estimated_minutes": int(est_session_minutes),
                    "break_pattern": break_pattern,
                    "created_at": __import__("time").time(),
                },
            )
            recent = recent[:10]
            update_current_session({"recent_sessions": recent})
            st.success("Time plan saved ✅")

        if session.get("recent_sessions"):
            st.markdown("##### Recent planned sessions")
            for s_item in session["recent_sessions"]:
                ts = __import__("time").strftime(
                    "%b %d, %Y",
                    __import__("time").localtime(s_item.get("created_at", __import__("time").time())),
                )
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
                reply = call_gemini_for_module("time", msg, session)
            st.session_state["ai_responses"]["time_plan"] = reply

        if st.session_state["ai_responses"].get("time_plan"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["time_plan"])
