# ui/components.py
import streamlit as st

def inject_css():
    st.markdown(
        """<style>
        .card{background:#E8F5E9;border:1px solid #d4eed8;border-radius:16px;padding:14px}
        .card-header{font-weight:700;margin-bottom:8px;color:#0D2B12}
        .chat-card{background:#E8F5E9;border:1px solid #d4eed8;border-radius:16px;overflow:hidden}
        .chat-header{background:#dff3e6;padding:12px 16px;font-weight:700;color:#0D2B12;border-bottom:1px solid #d4eed8}
        .chat-body{padding:14px 16px;height:420px;overflow-y:auto}
        .chat-input{border-top:1px solid #d4eed8;padding:12px 16px 16px}
        .chat-send .stButton>button{width:100%;background:#e95d55;color:#fff;border:none;padding:10px 14px;border-radius:10px}
        </style>""",
        unsafe_allow_html=True,
    )

def shell_left(st, state):
    with st.sidebar:
        st.title("🎓 Learning Toolkit")
        items = [
            ("goals","🎯 Goals"),
            ("task_analysis","📋 Task Analysis"),
            ("strategies","🧠 Strategies"),
            ("time_plan","⏰ Time Plan"),
            ("resources","📚 Resources"),
            ("reflection","🤔 Reflect"),
            ("feedback","✅ Feedback"),
        ]
        for key,label in items:
            if st.button(label, use_container_width=True):
                state.current_step = key
                st.rerun()

def chat_card(st, state):
    st.markdown("<div class='chat-card'>", unsafe_allow_html=True)
    st.markdown("<div class='chat-header'>Chat with Sylvia</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-body'>", unsafe_allow_html=True)
    for m in state.messages[-50:]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-input'>", unsafe_allow_html=True)
    user_text = st.chat_input("Describe your learning task or ask for guidance…")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-send'>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    return user_text
