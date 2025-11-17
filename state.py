"""
State management for the Thrive in Learning app.

This module encapsulates all mutations of ``st.session_state`` used by
the application. It provides functions for creating, loading, and
updating SRL sessions; managing which step is active; and updating
timer information. Keeping this logic in one place makes it easier to
modify how sessions are stored (for example, persisting to disk or
database) without changing the UI code.
"""

from __future__ import annotations

import time
import uuid
from typing import Dict, Any

import streamlit as st


def init_state() -> None:
    """Initialize all keys in ``st.session_state`` that the app relies on.

    This function should be called at the very beginning of the app.
    It sets up session storage, active step tracking, AI response cache,
    and timer metadata. If no sessions exist, a demo session is created.
    """
    if "sessions" not in st.session_state:
        st.session_state["sessions"] = {}

    if "current_session_id" not in st.session_state:
        # Create an initial demo session so the UI has some data to
        # display on first load. Students can create a new session
        # afterwards via the toolbar.
        create_new_session(default_demo=True)

    if "active_step" not in st.session_state:
        # Default to the first SRL step (goal setting)
        st.session_state["active_step"] = "goal"

    if "ai_responses" not in st.session_state:
        # Cache for storing the last AI reply per step
        st.session_state["ai_responses"] = {}

    # Timer state keys. The time step handles updating these values.
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_start_ts" not in st.session_state:
        st.session_state["timer_start_ts"] = None


def create_new_session(default_demo: bool = False) -> str:
    """Create a new SRL session and set it as the current session.

    Args:
        default_demo: if ``True``, populate the session with example
            values to show how the UI works on first run.

    Returns:
        The ID of the newly created session.
    """
    sid = str(uuid.uuid4())
    now = time.time()

    if default_demo:
        session = {
            "id": sid,
            "name": "Research paper on climate change",
            "created_at": now,
            "updated_at": now,
            "task_name": "Research paper on climate change",
            "task_type": "Research paper",
            "goal_type": "mastery",
            "goal_description": (
                "Deeply understand the mechanisms of climate change and "
                "their environmental impacts."
            ),
            "deadline": "",
            "requirements": "",
            "subtasks": "",
            "prior_knowledge": "",
            "knowledge_gaps": "",
            "anticipated_challenges": "",
            "contingency_plan": "",
            "chosen_strategies": [
                "Elaborative interrogation (ask why/how questions)",
                "Self‑explanation (teach it aloud or in writing)",
                "Concept mapping / diagrams",
            ],
            "session_plan": "",
            "recent_sessions": [],
            "resources": [],
            "reflections": {
                "goal": "",
                "strategies": "",
                "time": "",
                "growth": "",
            },
            "total_time_minutes": 0,
        }
    else:
        session = {
            "id": sid,
            "name": "New session",
            "created_at": now,
            "updated_at": now,
            "task_name": "",
            "task_type": "",
            "goal_type": "mastery",
            "goal_description": "",
            "deadline": "",
            "requirements": "",
            "subtasks": "",
            "prior_knowledge": "",
            "knowledge_gaps": "",
            "anticipated_challenges": "",
            "contingency_plan": "",
            "chosen_strategies": [],
            "session_plan": "",
            "recent_sessions": [],
            "resources": [],
            "reflections": {
                "goal": "",
                "strategies": "",
                "time": "",
                "growth": "",
            },
            "total_time_minutes": 0,
        }

    st.session_state["sessions"][sid] = session
    st.session_state["current_session_id"] = sid
    return sid


def get_current_session() -> Dict[str, Any]:
    """Return the currently active session.

    If the stored ``current_session_id`` is missing or invalid, a new
    session will be created automatically.
    """
    sid = st.session_state.get("current_session_id")
    sessions = st.session_state.get("sessions", {})
    if not sid or sid not in sessions:
        sid = create_new_session(default_demo=True)
    return sessions[sid]


def update_current_session(updates: Dict[str, Any]) -> None:
    """Update the current session with new values.

    Args:
        updates: a dictionary of keys and values to merge into the
            current session. The ``updated_at`` timestamp will be
            automatically refreshed.
    """
    session = get_current_session()
    session.update(updates)
    session["updated_at"] = time.time()
    st.session_state["sessions"][session["id"]] = session


def save_current_session() -> None:
    """Persist the current session to session storage.

    In this in‑memory implementation, updating the current session is
    effectively a no‑op because all changes are already reflected in
    ``st.session_state``. However, this function exists to support a
    future implementation where sessions might be written to disk or
    cloud storage. It also triggers a toast notification in the UI to
    confirm the save action.
    """
    # Even though nothing happens here, call update_current_session with
    # an empty dict to refresh the updated_at timestamp.
    update_current_session({})
    st.toast("Session saved ✅")


def delete_session(session_id: str) -> None:
    """Delete a session from storage.

    If the deleted session is the current one, the app will select
    another existing session (if available) or create a new empty one.

    Args:
        session_id: ID of the session to remove.
    """
    sessions = st.session_state.get("sessions", {})
    if session_id in sessions:
        del sessions[session_id]
    if st.session_state.get("current_session_id") == session_id:
        if sessions:
            # Pick the first remaining session
            st.session_state["current_session_id"] = next(iter(sessions.keys()))
        else:
            create_new_session(default_demo=False)


def start_timer() -> None:
    """Begin or resume the time tracker for the current session."""
    if not st.session_state.get("timer_running"):
        st.session_state["timer_running"] = True
        st.session_state["timer_start_ts"] = time.time()


def pause_timer() -> None:
    """Pause the time tracker and accumulate elapsed minutes."""
    if st.session_state.get("timer_running"):
        sync_timer_with_session()
        st.session_state["timer_running"] = False
        st.session_state["timer_start_ts"] = None


def reset_timer() -> None:
    """Reset the accumulated time for the current session."""
    update_current_session({"total_time_minutes": 0})
    st.session_state["timer_running"] = False
    st.session_state["timer_start_ts"] = None


def sync_timer_with_session() -> None:
    """Accumulate elapsed time (in whole minutes) into the current session.

    This function should be called on each app rerun to ensure that
    ongoing timers correctly update ``total_time_minutes``. It adds
    only whole minutes to avoid double‑counting seconds across rapid
    reruns.
    """
    if not st.session_state.get("timer_running"):
        return
    start_ts = st.session_state.get("timer_start_ts")
    if not start_ts:
        return
    now = time.time()
    elapsed_seconds = now - start_ts
    if elapsed_seconds <= 0:
        return
    minutes = int(elapsed_seconds // 60)
    if minutes > 0:
        session = get_current_session()
        current_minutes = int(session.get("total_time_minutes", 0))
        update_current_session({"total_time_minutes": current_minutes + minutes})
        # Set the new base for calculating elapsed time
        st.session_state["timer_start_ts"] = now


def format_time_from_minutes(total_minutes: int) -> str:
    """Format a minute count into HH:MM:SS for display."""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}:00"