import os

import streamlit as st
from PIL import Image

from state import init_app_state, get_current_session
from ui.components import inject_custom_css, render_header, render_session_toolbar, render_module_selector
from steps import STEPS, get_step_by_id


st.set_page_config(
    page_title="Thrive in Learning – SRL Companion",
    page_icon="🌱",
    layout="wide",
)


def main():
    init_app_state()
    inject_custom_css()

    # Optional sidebar logo
    if os.path.exists("bot.png"):
        with st.sidebar:
            st.image("bot.png", caption="Thrive in Learning", use_container_width=True)

    render_header()
    render_session_toolbar()

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        active_step_id = render_module_selector()

    with col_right:
        st.markdown('<div class="module-panel">', unsafe_allow_html=True)
        session = get_current_session()
        step = get_step_by_id(active_step_id)
        step.render(session)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
