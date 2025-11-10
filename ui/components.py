# ui/components.py - Comprehensive solution with verified CSS
import streamlit as st

def inject_css():
    st.markdown(
        """<style>
        /* Remove default Streamlit padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
        
        /* Target the left column specifically */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
            display: flex !important;
            flex-direction: column !important;
            min-height: 85vh !important;
        }
        
        /* Make the vertical block inside left column fill height */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child [data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
        }
        
        /* Target the radio group and make it spread */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio {
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
        }
        
        /* Distribute radio items evenly */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio > div {
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-around !important;
            height: 100% !important;
            padding: 2rem 0 !important;
        }
        
        /* Style individual radio items with spacing */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio label {
            padding: 1rem !important;
            margin: 0.75rem 0 !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            background: #f8fafc !important;
            border: 2px solid transparent !important;
            font-size: 15px !important;
        }
        
        /* Hover effect */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio label:hover {
            background: #e8f5e9 !important;
            border-color: #c8e6c9 !important;
            transform: translateX(4px) !important;
        }
        
        /* Selected state */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio input:checked ~ label,
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child .stRadio label:has(input:checked) {
            background: #e8f5e9 !important;
            border-color: #66bb6a !important;
            font-weight: 600 !important;
            box-shadow: 0 2px 8px rgba(102, 187, 106, 0.2) !important;
        }
        
        /* Ensure the Steps heading doesn't take extra space */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child h3 {
            margin-bottom: 1rem !important;
            flex-shrink: 0 !important;
        }
        
        /* Goals section styling */
        [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child h4 {
            margin-top: auto !important;
            padding-top: 1.5rem !important;
            border-top: 2px solid #e0e0e0 !important;
            flex-shrink: 0 !important;
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
        
        /* Scrollbar styling for chat container */
        .stChatMessage::-webkit-scrollbar {
            width: 8px;
        }
        
        .stChatMessage::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .stChatMessage::-webkit-scrollbar-thumb {
            background: #81c784;
            border-radius: 10px;
        }
        
        .stChatMessage::-webkit-scrollbar-thumb:hover {
            background: #66bb6a;
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
