"""
Reusable UI components for the Thrive in Learning app.

This module provides helpers for injecting CSS, rendering the header
bar with session metadata, displaying the session toolbar (save,
create, load and delete sessions), and rendering the list of SRL
modules as selectable buttons. Keeping UI code separate from the
business logic in ``state.py`` and ``services/ai.py`` makes it easy to
modify the look and feel without touching the underlying logic.
"""

from __future__ import annotations

import os
from typing import Optional

import streamlit as st

from state import (
    save_current_session,
    create_new_session,
    delete_session,
)


def inject_custom_css() -> None:
    """Inject custom CSS into the Streamlit app.

    If a file named ``mockup.css`` exists in the project root, its
    contents will be injected. Otherwise a minimal fallback style is
    applied to approximate the design from the provided HTML mockup.
    This function should be called exactly once before any UI is
    drawn. It relies on ``st.markdown`` with ``unsafe_allow_html`` to
    embed a ``<style>`` tag.
    """
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mockup.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    else:
        # Use a fallback style based on the provided mockup. In addition to the
        # original variables and component styles, remove Streamlit's default
        # side margins and width constraints so the app can occupy the full
        # browser width.
        css = """
        :root {
            --color-primary: #2563eb;
            --color-primary-dark: #1e40af;
            --color-primary-light: #dbeafe;
            --color-bg-alt: #f9fafb;
            --color-surface: #ffffff;
            --color-border: #aac2f2;
            --color-text: #1f2937;
            --color-text-secondary: #6b7280;
            --radius-lg: 0.75rem;
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        }
        body {
            background: var(--color-bg-alt);
        }
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
            box-shadow: var(--shadow-md);
        }

        /* Remove Streamlit's default side padding and width constraints for full-width layout */
        html, body {
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* Target Streamlit's main container elements */
        .main, .main > div {
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Remove padding from the block container */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
            padding-bottom: 0 !important;
            max-width: none !important;
        }
        
        /* Ensure the app view container takes full width */
        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }
        
        /* Remove any default Streamlit padding from the main content area */
        section[data-testid="stSidebar"] + div,
        section.main > div {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Ensure columns take full width */
        [data-testid="column"] {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header(session: dict) -> None:
    """Render the top header bar with logo and session metadata."""
    task_name = session.get("task_name") or session.get("name") or "New session"
    goal_type = session.get("goal_type", "mastery").title()
    time_minutes = session.get("total_time_minutes", 0)
    with st.container():
        st.markdown(
            f"""
            <div class="app-header">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
                <div class="app-logo">
                    <span>🌱</span>
                    <span>Thrive in Learning</span>
                </div>
                <div style="display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;font-size:.8rem;">
                    <span class="pill">📝 <span>{task_name}</span></span>
                    <span class="pill">🎯 <span>{goal_type} goal</span></span>
                    <span class="pill">⏱️ <span>{time_minutes} min logged</span></span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_session_toolbar() -> None:
    """Render the toolbar with actions to save, create, and manage sessions."""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("💾 Save session", use_container_width=True):
            save_current_session()
    with col2:
        if st.button("➕ New session", use_container_width=True):
            create_new_session(default_demo=False)
            # Clear cached AI responses when starting a new session
            st.session_state.get("ai_responses", {}).clear()
            st.session_state["timer_running"] = False
            st.session_state["timer_start_ts"] = None
            st.toast("New session created 🌱")
    with col3:
        # Expander for listing and managing existing sessions
        with st.expander("📂 Sessions", expanded=False):
            sessions = st.session_state.get("sessions", {})
            if not sessions:
                st.caption("No saved sessions yet.")
            else:
                current_sid = st.session_state.get("current_session_id")
                # Sort sessions by most recent update
                sorted_items = sorted(
                    sessions.items(), key=lambda item: item[1].get("updated_at", 0), reverse=True
                )
                for sid, sess in sorted_items:
                    label = sess.get("task_name") or sess.get("name") or "Untitled"
                    is_current = sid == current_sid
                    cols = st.columns([4, 1, 1])
                    cols[0].markdown(
                        f"**{label}**" + ("  ✅" if is_current else "")
                    )
                    if cols[1].button("Load", key=f"load_{sid}"):
                        st.session_state["current_session_id"] = sid
                        # Reset timer state to avoid mixing sessions
                        st.session_state["timer_running"] = False
                        st.session_state["timer_start_ts"] = None
                        st.experimental_rerun()
                    if cols[2].button("🗑️", key=f"delete_{sid}"):
                        delete_session(sid)
                        st.experimental_rerun()


def render_module_selector(active_step: Optional[str]) -> str:
    """Render the list of SRL modules and return the selected module ID.

    The selection is stored in ``st.session_state['active_step']``. Each
    module is displayed as a button with an optional description when
    active. Buttons are created in the order defined by ``steps.STEPS``.

    Args:
        active_step: the identifier of the currently selected module.

    Returns:
        The ID of the module selected by the user.
    """
    # Import steps lazily to avoid circular imports at module load time
    from steps import STEPS

    st.markdown("#### Learning modules")
    selected_id = active_step or (STEPS[0].id if STEPS else None)
    for step in STEPS:
        is_active = step.id == selected_id
        label = f"{step.emoji}  {step.label}"
        button_label = f"**{label}**" if is_active else label
        if st.button(button_label, key=f"module_{step.id}", use_container_width=True):
            selected_id = step.id
        if is_active:
            st.caption(step.description)
    return selected_id
