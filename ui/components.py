# ui/components.py
import streamlit as st

def inject_css():
    st.markdown(
        """<style>
        /* Remove default Streamlit padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        
        /* Add spacing between radio button items */
        .stRadio > div {
            gap: 1.5rem !important;
        }
        
        /* Style each radio button label */
        .stRadio label {
            padding: 0.75rem 1rem !important;
            margin: 0.5rem 0 !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: #f8fafc !important;
            border: 2px solid transparent !important;
            display: block !important;
        }
        
        /* Hover effect for radio options */
        .stRadio label:hover {
            background: #e8f5e9 !important;
            border-color: #c8e6c9 !important;
            transform: translateX(4px) !important;
        }
        
        /* Selected radio option styling */
        .stRadio input:checked + div label,
        .stRadio label:has(input:checked) {
            background: #e8f5e9 !important;
            border-color: #66bb6a !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(102, 187, 106, 0.2) !important;
        }
        
        /* Ensure radio buttons have proper spacing */
        .stRadio [role="radiogroup"] > label {
            margin-bottom: 1rem !important;
        }
        
        /* Card styles */
        .card{
            background:#E8F5E9;
            border:1px solid #d4eed8;
            border-radius:16px;
            padding:14px;
            margin-bottom: 1rem;
        }
        .card-header{
            font-weight:700;
            margin-bottom:8px;
            color:#0D2B12;
        }
        
        /* Chat header styling */
        .chat-header{
            background:#dff3e6;
            padding:12px 16px;
            font-weight:700;
            color:#0D2B12;
            border: 1px solid #d4eed8;
            border-radius: 12px 12px 0 0;
            margin-bottom: 0;
            margin-top: 1rem;
        }
        
        /* Compact chat message styling */
        .stChatMessage {
            padding: 0.5rem 0 !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Hide the default chat input label */
        .stChatInput label {
            display: none !important;
        }
        
        /* Remove extra spacing */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* Adjust button styling */
        .stButton>button{
            width:100%;
            background:#e95d55;
            color:#fff;
            border:none;
            padding:10px 14px;
            border-radius:10px;
            transition: all 0.2s;
        }
        
        .stButton>button:hover{
            background:#d54d45;
            transform: translateY(-1px);
        }
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
    # Chat header
    st.markdown("<div class='chat-header'>Chat with Sylvia</div>", unsafe_allow_html=True)
    
    # Create a container with fixed height for scrolling
    with st.container(height=400, border=True):
        # Display all messages
        for m in state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
    
    # Chat input at the bottom
    user_text = st.chat_input("Describe your learning task or ask for guidance…")
    
    return user_text
