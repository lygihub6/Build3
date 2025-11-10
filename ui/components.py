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
        
        /* Make the left column stretch full height and distribute content */
        [data-testid="column"]:first-child {
            display: flex !important;
            flex-direction: column !important;
            min-height: calc(100vh - 4rem) !important;
        }
        
        /* Style the Steps section */
        [data-testid="column"]:first-child > div {
            display: flex;
            flex-direction: column;
            flex: 1;
        }
        
        /* Distribute radio buttons evenly with spacing */
        [data-testid="column"]:first-child .stRadio {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 !important;
            justify-content: space-evenly !important;
            padding: 2rem 0 !important;
        }
        
        /* Space out individual radio items */
        [data-testid="column"]:first-child .stRadio > div {
            display: flex !important;
            flex-direction: column !important;
            gap: 1.5rem !important;
        }
        
        /* Make each radio option larger and more prominent */
        [data-testid="column"]:first-child .stRadio label {
            padding: 0.75rem 1rem !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: #f8fafc !important;
            border: 2px solid transparent !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Hover effect for radio options */
        [data-testid="column"]:first-child .stRadio label:hover {
            background: #e8f5e9 !important;
            border-color: #d4eed8 !important;
        }
        
        /* Selected radio option */
        [data-testid="column"]:first-child .stRadio input:checked + div {
            background: #e8f5e9 !important;
            border-color: #81c784 !important;
            font-weight: 600 !important;
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
        }
        
        /* Chat container */
        .chat-container {
            border: 1px solid #d4eed8;
            border-top: none;
            border-radius: 0 0 12px 12px;
            background: #E8F5E9;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Custom scrollbar for the container */
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stChatMessage"])::-webkit-scrollbar {
            width: 8px;
        }
        
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stChatMessage"])::-webkit-scrollbar-track {
            background: #d4eed8;
            border-radius: 10px;
        }
        
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stChatMessage"])::-webkit-scrollbar-thumb {
            background: #81c784;
            border-radius: 10px;
        }
        
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stChatMessage"])::-webkit-scrollbar-thumb:hover {
            background: #66bb6a;
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
        
        /* Goals section at bottom of sidebar */
        [data-testid="column"]:first-child h4 {
            margin-top: auto;
            padding-top: 2rem;
            border-top: 2px solid #e8f5e9;
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
    # The height parameter makes it scrollable automatically
    with st.container(height=400, border=True):
        # Display all messages
        for m in state.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
    
    # Chat input at the bottom (outside the scrollable container)
    user_text = st.chat_input("Describe your learning task or ask for guidance…")
    
    return user_text
