import time
import uuid
from typing import Dict, Any

import streamlit as st


def init_app_state():
    if "sessions" not in st.session_state:
        st.session_state["sessions"] = {}
    if "current_session_id" not in st.session_state:
        create_new_session(default_demo=True)
    if "active_step" not in st.session_state:
        st.session_state["active_step"] = "goals"
    if "ai_responses" not in st.session_state:
        st.session_state["ai_responses"] = {}
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "timer_start_ts" not in st.session_state:
        st.session_state["timer_start_ts"] = None


def create_new_session(default_demo: bool = False) -> str:
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
                "Deeply understand the mechanisms of climate change and their environmental impacts."
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
                "Self-explanation (teach it aloud or in writing)",
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
    sid = st.session_state.get("current_session_id")
    sessions = st.session_state.get("sessions", {})
    if not sid or sid not in sessions:
        sid = create_new_session(default_demo=True)
    return st.session_state["sessions"][sid]


def update_current_session(updates: Dict[str, Any]):
    session = get_current_session()
    session.update(updates)
    session["updated_at"] = time.time()
    st.session_state["sessions"][session["id"]] = session


def save_session_snapshot():
    get_current_session()
    update_current_session({})
    st.toast("Session saved ✅")


def delete_session(session_id: str):
    sessions = st.session_state.get("sessions", {})
    if session_id in sessions:
        del sessions[session_id]
    if st.session_state.get("current_session_id") == session_id:
        if sessions:
            st.session_state["current_session_id"] = next(iter(sessions.keys()))
        else:
            create_new_session(default_demo=False)


def format_time_from_minutes(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}:00"


def sync_timer_with_session():
    if not st.session_state.get("timer_running"):
        return
    start_ts = st.session_state.get("timer_start_ts")
    if not start_ts:
        return
    now = time.time()
    elapsed = now - start_ts
    if elapsed <= 0:
        return
    minutes = int(elapsed // 60)
    if minutes > 0:
        session = get_current_session()
        current = int(session.get("total_time_minutes", 0))
        update_current_session({"total_time_minutes": current + minutes})
        st.session_state["timer_start_ts"] = now
