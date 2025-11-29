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

from .base import BaseStep
from services.ai import safe_ai


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

        # ========== CACHE MANAGEMENT SECTION ==========
        # Add cache clearing functionality to help users recover from cached errors
        with st.expander("⚙️ Troubleshooting & Cache Settings", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Show cache stats
                cache_size = len(st.session_state.get("ai_cache", {}))
                st.caption(f"**Cached responses:** {cache_size}")
                st.caption(
                    "💡 Clear the cache if you've changed your API key, "
                    "see old error messages, or want completely fresh responses."
                )
            
            with col2:
                # Cache clear button
                if st.button("🔄 Clear Cache", key="clear_ai_cache", use_container_width=True):
                    # Clear AI cache
                    if "ai_cache" in st.session_state:
                        st.session_state["ai_cache"] = {}
                    if "ai_last_call_ts" in st.session_state:
                        st.session_state["ai_last_call_ts"] = 0.0
                    # Clear cached AI responses in this module
                    if "ai_responses" in st.session_state and self.id in st.session_state["ai_responses"]:
                        del st.session_state["ai_responses"][self.id]
                    
                    st.success("✅ Cache cleared successfully!")
                    st.info("Try your request again - it will now make a fresh API call.")
                    st.rerun()

        # ========== MAIN FEEDBACK INPUT ==========
        msg = st.text_area(
            "Describe any patterns you're noticing or questions you have about your study habits.",
            key="feedback_input",
            height=150,
            placeholder="Example: I notice I get distracted easily when studying in the evening. How can I improve my focus?"
        )

        # ========== GET FEEDBACK BUTTON ==========
        if st.button("💬 Get feedback", key="feedback_button", type="primary") and msg.strip():
            # Use the safe AI wrapper to generate supportive feedback
            # with caching and simple rate limiting, consistent with other steps.
            with st.spinner("Gathering feedback..."):
                reply = safe_ai(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        # ========== DISPLAY AI RESPONSE ==========
        # Display last AI response, if available
        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("---")
            st.markdown("##### 🤖 AI Suggestion")
            
            response_text = st.session_state["ai_responses"][self.id]
            st.markdown(response_text)
            
            # ========== HELPFUL HINTS FOR ERRORS ==========
            # Show a hint if the response looks like an error
            if "⚠️" in response_text or "error" in response_text.lower():
                st.markdown("---")
                st.warning(
                    "**💡 Troubleshooting Tip:**\n\n"
                    "If you see an error above but have already fixed the issue "
                    "(e.g., changed your API key or waited for quota reset), "
                    "the error might be **cached**.\n\n"
                    "**Solution:** Click the **'🔄 Clear Cache'** button in the "
                    "'Troubleshooting & Cache Settings' section above, then try again."
                )
