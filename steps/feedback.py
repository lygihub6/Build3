"""
Feedback step implementation.

This optional module allows students to request high-level feedback on
their overall study habits or their use of the app. It exposes a
single text input where the student can describe their situation or
concerns and then calls the Gemini API to generate supportive,
constructive feedback.
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict

# Add this import at the top
from services.ai import safe_ai

# Add this code before the "Get feedback" button
if st.button("🔄 Clear AI cache", key="clear_cache_button"):
    if "ai_cache" in st.session_state:
        st.session_state["ai_cache"] = {}
    if "ai_last_call_ts" in st.session_state:
        st.session_state["ai_last_call_ts"] = 0.0
    st.success("Cache cleared! Try your request again.")
    st.rerun()

from .base import BaseStep

class FeedbackStep(BaseStep):
    """Feedback SRL step."""

    id = "feedback"
    label = "Feedback"
    emoji = "📝"
    description = "High-level feedback on your study habits and app use."

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("📝 Feedback")
        st.markdown(
            "This section lets you ask for general feedback on your study habits, "
            "use of strategies, or anything else related to learning."
        )

        # Add cache management controls in an expander
        with st.expander("⚙️ Advanced Settings", expanded=False):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.caption(f"Cached responses: {get_cache_size()}")
                st.caption(
                    "Clear the cache if you've changed your API key or want fresh responses."
                )
            with col2:
                if st.button("🔄 Clear cache", key="clear_ai_cache"):
                    clear_ai_cache()
                    st.success("Cache cleared!")
                    st.rerun()

        msg = st.text_area(
            "Describe any patterns you're noticing or questions you have about your study habits.",
            key="feedback_input",
            height=150,
        )

        if st.button("💬 Get feedback", key="feedback_button") and msg.strip():
            # Use the safe AI wrapper to generate supportive feedback
            # with caching and simple rate limiting, consistent with other steps.
            with st.spinner("Gathering feedback..."):
                reply = safe_ai(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        # Display last AI response, if available
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])
            
            # Show a hint if the response looks like an error
            if "⚠️" in st.session_state["ai_responses"][self.id]:
                st.info(
                    "💡 **Tip:** If you see an error message but have already fixed the issue "
                    "(e.g., changed your API key), try clearing the cache above and submitting again."
                )
