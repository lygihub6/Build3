# ui/components.py
import streamlit as st
from datetime import datetime

def inject_css():
    st.markdown(
        """<style>
        /* Remove default padding and maximize space */
        .main .block-container {
            padding: 0.5rem 0.5rem 0 0.5rem !important;
            max-width: 100% !important;
        }
        
        .stApp {
            background-color: #f5f5f5;
        }
        
        /* Column styling */
        [data-testid="column"] {
            padding: 0.5rem !important;
        }
        
        /* Left sidebar styling */
        [data-testid="column"]:first-child {
            background: linear-gradient(180deg, #d4ecd4 0%, #c8e6c8 100%);
            border-radius: 12px;
            padding: 1rem !important;
        }
        
        /* Center column */
        [data-testid="column"]:nth-child(2) {
            background: white;
            border-radius: 12px;
            padding: 0 !important;
        }
        
        /* Right sidebar */
        [data-testid="column"]:last-child {
            background: transparent;
            padding: 0.5rem !important;
        }
        
        /* Hide streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            background: rgba(255, 255, 255, 0.6);
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            text-align: left;
            font-weight: 500;
            color: #2a5a2a;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background: rgba(255, 255, 255, 0.9);
            transform: translateX(2px);
        }
        
        /* Section headers */
        .section-header {
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            color: #5a8a5a;
            letter-spacing: 0.5px;
            margin: 1.5rem 0 0.75rem 0;
        }
        
        /* Timer styling */
        .timer-display {
            background: rgba(255, 255, 255, 0.6);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            margin: 1rem 0;
        }
        
        .timer-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2a5a2a;
            font-family: 'Courier New', monospace;
        }
        
        /* Upload area */
        .upload-box {
            background: rgba(255, 255, 255, 0.4);
            border: 2px dashed #b8e0b8;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            margin-top: 1rem;
        }
        
        /* Chat messages */
        .stChatMessage {
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        
        [data-testid="stChatMessageContent"] {
            padding: 0.75rem 1rem;
        }
        
        /* Chat input */
        .stChatInput {
            border-radius: 24px;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #2a5a2a 0%, #4a7c4a 100%);
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Step items */
        .step-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: white;
            border-radius: 8px;
            margin-bottom: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .step-item:hover {
            background: #f9f9f9;
        }
        
        .step-number {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #e8f5e8;
            color: #2a5a2a;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9rem;
            flex-shrink: 0;
        }
        
        .step-number.completed {
            background: #2a5a2a;
            color: white;
        }
        
        /* Remove extra spacing */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: white;
            border-radius: 8px;
            font-weight: 600;
        }
        </style>""",
        unsafe_allow_html=True,
    )

def render_left_sidebar(st, state, REGISTRY):
    """Render the left sidebar with actions, timer, and upload"""
    
    # Logo and tagline
    st.markdown("# 🎓 Sylvia")
    st.caption("Your personal learning facilitator, designed to help you develop mastery goals, effective learning strategies, and self-regulated learning capacities for deep, meaningful learning.")
    
    # Learning Actions
    st.markdown("<div class='section-header'>LEARNING ACTIONS</div>", unsafe_allow_html=True)
    
    if REGISTRY:
        for step_key, step_module in REGISTRY.items():
            if st.button(f"{step_module.icon} {step_module.label}", key=f"action_{step_key}"):
                state.current_step = step_key
                # Mark as visited
                for path_step in state.learning_path:
                    if path_step['id'] == step_key:
                        path_step['completed'] = True
                        break
                # Update progress
                completed = sum(1 for s in state.learning_path if s['completed'])
                state.progress_percent = int((completed / len(state.learning_path)) * 100)
                st.rerun()
    
    # Support Section
    st.markdown("<div class='section-header'>SUPPORT</div>", unsafe_allow_html=True)
    if st.button("📚 Resources", key="support_resources"):
        state.current_step = "resources"
        st.rerun()
    if st.button("💭 Reflect", key="support_reflect"):
        state.current_step = "reflection"
        st.rerun()
    if st.button("✅ Feedback", key="support_feedback"):
        state.current_step = "feedback"
        st.rerun()
    
    # Process Monitor
    st.markdown("<div class='section-header'>PROCESS MONITOR</div>", unsafe_allow_html=True)
    if st.button("📝 Time Log", key="time_log"):
        st.info("Time log feature - track your learning sessions!")
    
    # Timer
    st.markdown("<div class='timer-display'>", unsafe_allow_html=True)
    timer_col1, timer_col2, timer_col3 = st.columns(3)
    
    with timer_col1:
        if st.button("Start", key="timer_start", use_container_width=True):
            state.timer_running = True
    with timer_col2:
        if st.button("Pause", key="timer_pause", use_container_width=True):
            state.timer_running = False
    with timer_col3:
        if st.button("Reset", key="timer_reset", use_container_width=True):
            state.timer_minutes = 25
            state.timer_seconds = 0
            state.timer_running = False
    
    st.markdown(f"<div class='timer-number'>{state.timer_minutes:02d}:{state.timer_seconds:02d}</div>", unsafe_allow_html=True)
    
    # Timer presets
    preset_col1, preset_col2, preset_col3 = st.columns(3)
    with preset_col1:
        if st.button("25m", key="preset_25"):
            state.timer_minutes = 25
            state.timer_seconds = 0
    with preset_col2:
        if st.button("15m", key="preset_15"):
            state.timer_minutes = 15
            state.timer_seconds = 0
    with preset_col3:
        if st.button("5m", key="preset_5"):
            state.timer_minutes = 5
            state.timer_seconds = 0
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Upload Materials
    st.markdown("<div class='section-header'>UPLOAD MATERIALS</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop files here or click to browse",
        type=['pdf', 'docx', 'txt', 'png', 'jpg'],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

def render_chat_area(st, state):
    """Render the center chat area"""
    
    # Chat header
    st.markdown("## 💬 Chat with Sylvia")
    st.markdown("---")
    
    # Messages container
    for msg in state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input at bottom
    user_input = st.chat_input("Type your message here...")
    
    return user_input

def render_right_sidebar(st, state):
    """Render the right sidebar with learning path, progress, and sessions"""
    
    # Learning Path
    with st.container():
        st.markdown("### 🎯 Learning Path")
        
        for idx, step in enumerate(state.learning_path):
            col1, col2 = st.columns([0.15, 0.85])
            
            with col1:
                if step['completed']:
                    st.markdown(f"<div class='step-number completed'>✓</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='step-number'>{idx + 1}</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"**{step['name']}**")
                st.caption(step['desc'])
            
            if idx < len(state.learning_path) - 1:
                st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    st.markdown("&nbsp;")
    
    # Progress Section
    with st.container():
        st.markdown("### 🎯 Progress")
        st.markdown(f"**Task Completion** — {state.progress_percent}%")
        st.progress(state.progress_percent / 100)
    
    st.markdown("&nbsp;")
    
    # Session Management
    with st.container():
        st.markdown("### 📋 Session")
        
        if st.button("🗑️ Clear", use_container_width=True):
            state.messages = []
            state.progress_percent = 0
            for step in state.learning_path:
                step['completed'] = False
            st.rerun()
        
        if st.button("💾 Save Session", use_container_width=True):
            session_name = f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            state.saved_sessions.append({
                'name': session_name,
                'time': datetime.now(),
                'messages': state.messages.copy(),
                'progress': state.progress_percent
            })
            st.success("Session saved!")
        
        if st.button("📤 Export", use_container_width=True):
            # Create export of conversation
            export_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in state.messages])
            st.download_button(
                label="Download Chat History",
                data=export_text,
                file_name=f"sylvia_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )
        
        if st.button("➕ New Session", use_container_width=True):
            # Save current session first
            if state.messages:
                session_name = f"Auto-saved {datetime.now().strftime('%H:%M')}"
                state.saved_sessions.append({
                    'name': session_name,
                    'time': datetime.now(),
                    'messages': state.messages.copy(),
                    'progress': state.progress_percent
                })
            # Clear for new session
            state.messages = []
            state.progress_percent = 0
            for step in state.learning_path:
                step['completed'] = False
            st.rerun()
    
    st.markdown("&nbsp;")
    
    # Saved Sessions
    if state.saved_sessions:
        with st.container():
            st.markdown("### 📁 Saved Sessions")
            
            for idx, session in enumerate(reversed(state.saved_sessions[-5:])):  # Show last 5
                with st.expander(session['name']):
                    st.caption(f"Progress: {session['progress']}%")
                    st.caption(f"Messages: {len(session['messages'])}")
                    if st.button("Load", key=f"load_session_{idx}"):
                        state.messages = session['messages'].copy()
                        state.progress_percent = session['progress']
                        st.rerun()

def shell_left(st, state):
    """Legacy function for compatibility"""
    pass

def chat_card(st, state):
    """Legacy function for compatibility"""
    return None
