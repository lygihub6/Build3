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
        
        /* Chat section styles */
        .chat-section {
            background:#E8F5E9;
            border:1px solid #d4eed8;
            border-radius:16px;
            padding: 0;
            margin-top: 1rem;
            overflow: hidden;
        }
        
        .chat-header{
            background:#dff3e6;
            padding:12px 16px;
            font-weight:700;
            color:#0D2B12;
            border-bottom:1px solid #d4eed8;
            margin: 0;
        }
        
        /* Remove extra spacing around chat messages */
        .stChatMessage {
            padding: 0.5rem 1rem;
        }
        
        /* Chat input styling */
        .stChatInput {
            border-top:1px solid #d4eed8;
        }
        
        /* Hide the default chat input label */
        .stChatInput label {
            display: none;
        }
        
        /* Compact the chat container */
        [data-testid="stChatMessageContainer"] {
            max-height: 400px;
            overflow-y: auto;
            padding: 0.5rem;
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
    # Chat header without wrapping divs
    st.markdown("""
        <div class='chat-section'>
            <div class='chat-header'>Chat with Sylvia</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a container for messages with limited height
    with st.container():
        # Display recent messages
        for m in state.messages[-20:]:  # Limit to last 20 messages to avoid clutter
            with st.chat_message(m["role"]):
                st.markdown(m["content"])
    
    # Chat input at the bottom
    user_text = st.chat_input("Describe your learning task or ask for guidance…")
    
    return user_text
