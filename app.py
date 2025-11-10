# app.py
import streamlit as st
from datetime import datetime, timedelta
from state import get_state

# Components
from ui.components import (
    inject_css, 
    render_left_sidebar, 
    render_chat_area,
    render_right_sidebar
)

# Steps registry (safe import)
try:
    from steps import REGISTRY
except Exception as e:
    REGISTRY = {}
    print(f"[app] Steps failed to load: {e}")

# AI call (safe import + graceful fallback)
try:
    from services.ai import chat_once
    _ai_ok = True
except Exception as e:
    print(f"[app] AI service unavailable: {e}")
    _ai_ok = False

st.set_page_config(
    page_title="Sylvia – Your Learning Facilitator", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    state = get_state(st)
    inject_css()
    
    # Initialize state variables if they don't exist
    if not hasattr(state, 'timer_minutes'):
        state.timer_minutes = 25
    if not hasattr(state, 'timer_seconds'):
        state.timer_seconds = 0
    if not hasattr(state, 'timer_running'):
        state.timer_running = False
    if not hasattr(state, 'progress_percent'):
        state.progress_percent = 0
    if not hasattr(state, 'saved_sessions'):
        state.saved_sessions = []
    if not hasattr(state, 'learning_path'):
        state.learning_path = [
            {'id': 'goals', 'name': 'Goals', 'desc': 'Define mastery goals', 'completed': False},
            {'id': 'task_analysis', 'name': 'Task Analysis', 'desc': 'Break down the task', 'completed': False},
            {'id': 'strategies', 'name': 'Strategies', 'desc': 'Plan your approach', 'completed': False},
            {'id': 'time_plan', 'name': 'Time Plan', 'desc': 'Schedule your work', 'completed': False},
            {'id': 'resources', 'name': 'Resources', 'desc': 'Find materials', 'completed': False},
            {'id': 'reflection', 'name': 'Reflection', 'desc': 'Reflect on learning', 'completed': False},
            {'id': 'feedback', 'name': 'Feedback', 'desc': 'Get feedback', 'completed': False},
        ]
    
    # Add initial message if messages is empty
    if not state.messages:
        state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm Sylvia, your learning facilitator. I'm here to help you develop effective learning strategies and achieve your academic goals through self-regulated learning. What task are you working on today?"
        })
    
    # --- 3 Column Layout ---
    left_col, center_col, right_col = st.columns([1, 2.5, 1.3], gap="small")
    
    # LEFT SIDEBAR
    with left_col:
        render_left_sidebar(st, state, REGISTRY)
    
    # CENTER CHAT AREA
    with center_col:
        user_text = render_chat_area(st, state)
        
        # Handle new messages
        if user_text:
            state.messages.append({"role": "user", "content": user_text})
            
            # Call AI model
            if _ai_ok:
                try:
                    from google.genai import types
                    parts = [
                        types.Content(
                            role=("user" if m["role"] == "user" else "model"),
                            parts=[types.Part(text=m["content"])],
                        )
                        for m in state.messages[-10:]
                    ]
                    resp = chat_once(parts)
                    text = getattr(resp, "text", None) or "I'm here to help."
                except Exception as e:
                    text = f"I'm having trouble connecting right now. Let me try to help anyway: I understand you're working on something. Could you tell me more about your learning goals for this task?"
            else:
                text = "I'm here to help you develop effective learning strategies. Could you tell me more about what you're working on?"
            
            state.messages.append({"role": "assistant", "content": text})
            st.rerun()
    
    # RIGHT SIDEBAR
    with right_col:
        render_right_sidebar(st, state)

if __name__ == "__main__":
    main()
