"""
Main entrypoint for the Thrive in Learning Streamlit application.

This script wires together the session state, UI components, and
individual self‑regulated learning (SRL) steps. It sets up the page,
loads the system prompt from ``identity.txt``, initializes internal
state, and delegates rendering to the appropriate module based on the
current step the student has selected.

The application is designed to be modular and extensible: new steps
can be added simply by creating a new file in ``steps/`` that defines
a subclass of ``BaseStep`` and registering it in ``steps/__init__.py``.

The current implementation includes the following steps:

* Tutorial (welcome and instructions)
* Goal setting
* Task analysis
* Learning strategies
* Time planning
* Resources
* Reflection

Each step is responsible for rendering its own UI elements and calling
the Gemini API via the helper exposed in ``services/ai.py`` when
appropriate.
"""
from __future__ import annotations

import streamlit as st

from state import (
    init_state,
    get_current_session,
)

from ui.components import (
    inject_custom_css,
    render_header,
    render_session_toolbar,
    render_module_selector,
)

from steps import STEPS, get_step_by_id


def main():
    st.set_page_config(
        page_title="Thrive in Learning",
        page_icon="🌱",
        layout="wide",
    )

    # --- Initialize state + get the current SRL session ---
    init_state()
    session = get_current_session()

    # --- Inject custom CSS once, before drawing the UI ---
    inject_custom_css()

    # --- Top toolbar + header bar ---
    render_session_toolbar()   # 💾 Save / ➕ New / 📂 Sessions
    render_header(session)     # 🌱 logo + task name + goal type + time

    # --- Main layout: modules on the left, active step on the right ---
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
    st.markdown("#### Learning modules")
    default_step = st.session_state.get("active_step", STEPS[0].id)
    active_step_id = render_module_selector(default_step)
    st.session_state["active_step"] = active_step_id


    with right_col:
        # Card-style container for the module content
        st.markdown('<div class="module-panel">', unsafe_allow_html=True)
        step = get_step_by_id(active_step_id)
        if step:
            step.render(session)
        else:
            st.info("Pick a module on the left to begin.")
        st.markdown("</div>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
