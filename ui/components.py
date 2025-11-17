import os
import time
import streamlit as st

from state import (
    get_current_session,
    save_session_snapshot,
    delete_session,
)


def inject_custom_css():
    css_path = "mockup.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    else:
        css = """
        :root {
            --color-primary: #2563eb;
            --color-primary-light: #dbeafe;
            --color-bg-alt: #f9fafb;
            --color-surface: #ffffff;
            --color-border: #e5e7eb;
            --color-text: #1f2937;
            --color-text-secondary: #6b7280;
        }
        body { background: var(--color-bg-alt); }
        .app-header {
            background: var(--color-surface);
            border-bottom: 1px solid var(--color-border);
            padding: 0.75rem 1.5rem;
            margin: -1rem -1rem 1rem -1rem;
        }
        .app-logo {
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--color-primary);
            display: flex;
            align-items: center;
            gap: .5rem;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            font-size: 0.8rem;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            border: 1px solid var(--color-border);
            color: var(--color-text-secondary);
            gap: 0.25rem;
            margin-right: 0.35rem;
        }
        .module-panel {
            background: var(--color-surface);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1),
                        0 2px 4px -1px rgba(0,0,0,0.06);
        }
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header():
    session = get_current_session()
    session_name = session.get("task_name") or session.get("name") or "New session"
    total_min = int(session.get("total_time_minutes", 0))
    goal_type = session.get("goal_type", "mastery").title()

    st.markdown(
        f"""
        <div class="app-header">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
            <div class="app-logo">
                <span>🌱</span>
                <span>Thrive in Learning</span>
            </div>
            <div style="display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;font-size:.8rem;">
                <span class="pill">📝 <span>{session_name}</span></span>
                <span class="pill">🎯 <span>{goal_type} goal</span></span>
                <span class="pill">⏱️ <span>{total_min} min logged</span></span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_session_toolbar():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("💾 Save session", use_container_width=True):
            save_session_snapshot()

    from state import create_new_session  # avoid circular import at module level
    with col2:
        if st.button("➕ New session", use_container_width=True):
            create_new_session(default_demo=False)
            st.session_state["ai_responses"] = {}
            st.session_state["timer_running"] = False
            st.session_state["timer_start_ts"] = None
            st.toast("New session created 🌱")

    with col3:
        with st.expander("📂 Sessions", expanded=False):
            sessions = st.session_state.get("sessions", {})
            if not sessions:
                st.caption("No saved sessions yet.")
            else:
                for sid, sess in sessions.items():
                    label = sess.get("task_name") or sess.get("name") or "Untitled"
                    is_current = sid == st.session_state.get("current_session_id")
                    c1, c2, c3 = st.columns([4, 1, 1])
                    c1.markdown(f"**{label}**" + ("  ✅" if is_current else ""))
                    if c2.button("Load", key=f"load_{sid}"):
                        st.session_state["current_session_id"] = sid
                        st.experimental_rerun()
                    if c3.button("🗑️", key=f"del_{sid}"):
                        delete_session(sid)
                        st.experimental_rerun()


MODULES = [
    {"id": "goals", "emoji": "🎯", "label": "Goal Setting"},
    {"id": "task_analysis", "emoji": "🔍", "label": "Task Analysis"},
    {"id": "strategies", "emoji": "💡", "label": "Learning Strategies"},
    {"id": "time_plan", "emoji": "⏱️", "label": "Time Management"},
    {"id": "resources", "emoji": "📚", "label": "Resources"},
    {"id": "reflection", "emoji": "✨", "label": "Reflection"},
    {"id": "feedback", "emoji": "🧠", "label": "Meta-Feedback"},
]


def render_module_selector() -> str:
    st.markdown("#### Learning modules")
    active = st.session_state.get("active_step", "goals")
    for m in MODULES:
        is_active = m["id"] == active
        label = f"{m['emoji']}  {m['label']}"
        if st.button(label if not is_active else f"**{label}**", key=f"nav_{m['id']}", use_container_width=True):
            st.session_state["active_step"] = m["id"]
            active = m["id"]
    return active
