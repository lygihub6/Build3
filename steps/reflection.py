"""
Reflection step implementation.

The reflection module guides students in evaluating their learning
process. It encourages them to consider how well they achieved their
goals, which strategies worked, how accurately they managed their
time and focus, and what they will do differently next time. An AI
assistant can ask deeper questions or highlight patterns.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from state import update_current_session
from services.ai import safe_ai
from .base import BaseStep


class ReflectionStep(BaseStep):
    """Reflection SRL step."""

    id = "reflection"
    label = "Reflection"
    emoji = "✨"
    description = "Evaluate your learning and celebrate your progress."

    def render(self, session: Dict[str, Any]) -> None:
        st.subheader("✨ Reflection")
        st.markdown(
            "Reflection helps you **close the loop**: connect what happened to what you want to change next time."
        )

        # Get any existing reflection for this session
        refs = session.get(
            "reflections",
            {"goal": "", "strategies": "", "time": "", "growth": ""},
        )

        # ---- Four reflection prompts (editable) ----
        goal_ref = st.text_area(
            "1. Goal achievement – What did you actually learn or understand? Did you reach your mastery goal?",
            value=refs.get("goal", ""),
            key="refl_goal",
            height=120,
        )
        strat_ref = st.text_area(
            "2. Strategies – Which strategies helped most? Which did you not use or found unhelpful?",
            value=refs.get("strategies", ""),
            key="refl_strategies",
            height=120,
        )
        time_ref = st.text_area(
            "3. Time & focus – How well did you stick to your plan? What affected your focus?",
            value=refs.get("time", ""),
            key="refl_time",
            height=120,
        )
        growth_ref = st.text_area(
            "4. Next steps – What will you do **differently** for the next similar task?",
            value=refs.get("growth", ""),
            key="refl_growth",
            height=120,
        )

        if st.button("Save reflection", key="save_reflection"):
            new_refs = {
                "goal": goal_ref.strip(),
                "strategies": strat_ref.strip(),
                "time": time_ref.strip(),
                "growth": growth_ref.strip(),
            }
            update_current_session({"reflections": new_refs})
            st.success("Reflection saved 🌱")
            # Note: `session` is updated via update_current_session, so the
            # summary block below will pick up the new values on this rerun.

        # ---- Show saved reflection summary (read-only) ----
        saved = session.get("reflections")
        if saved and any(saved.values()):
            st.markdown("---")
            st.markdown("##### Your saved reflection")
            with st.container():
                if saved.get("goal"):
                    st.markdown("**Goal achievement**")
                    st.markdown(f"> {saved['goal']}")
                if saved.get("strategies"):
                    st.markdown("**Strategies**")
                    st.markdown(f"> {saved['strategies']}")
                if saved.get("time"):
                    st.markdown("**Time & focus**")
                    st.markdown(f"> {saved['time']}")
                if saved.get("growth"):
                    st.markdown("**Next steps**")
                    st.markdown(f"> {saved['growth']}")

        st.markdown("---")
        st.markdown("##### Ask AI to deepen your reflection")

        msg = st.text_area(
            "Paste a short summary of what happened (or the text above), and the assistant will ask a few deeper questions or highlight patterns.",
            key="reflection_ai_input",
            height=150,
        )

        if st.button("🪞 Help me reflect", key="reflection_ai_button") and msg.strip():
            # Use the safe AI wrapper to deepen reflection with caching and rate limiting
            with st.spinner("Thinking with you about this experience..."):
                reply = safe_ai(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])
