"""
Learning strategies step implementation.

Students choose concrete strategies they plan to use for this task.
They can select from evidence-based strategies and also add their own.
An AI helper can suggest strategies based on the task description.
"""

from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st

from state import update_current_session
from services.ai import safe_ai
from .base import BaseStep


DEFAULT_STRATEGIES: List[str] = [
    "Elaborative interrogation (ask why/how questions)",
    "Self-explanation (teach it aloud or in writing)",
    "Spaced practice (short sessions over days)",
    "Practice testing (quiz yourself)",
    "Concept mapping / diagrams",
    "Worked examples then fading",
    "Interleaving different problem types",
    "Summarizing key ideas in your own words",
    "Teaching a friend / study buddy",
    "Creating and reviewing flashcards",
    "Doing challenge problems after basics",
]


class StrategiesStep(BaseStep):
    """Learning strategies SRL step."""

    id = "strategies"
    label = "Learning Strategies"
    emoji = "💡"
    description = "Select and refine how you’ll study for this task."

    def render(self, session: Dict[str, Any]) -> None:
        # -------- Clear the 'new strategy' input on the next run --------
        if st.session_state.get("clear_new_strategy_input"):
            if "new_strategy_text" in st.session_state:
                del st.session_state["new_strategy_text"]
            st.session_state["clear_new_strategy_input"] = False

        st.subheader("💡 Learning Strategies")
        st.markdown(
            "Select strategies you'd like to try for this task. "
            "Start with a few and actually use them."
        )

        # ---- Load previous selections from the SRL session ----
        stored = session.get("strategies", {})
        selected_existing: List[str] = stored.get("selected", [])
        custom_strats: List[str] = stored.get("custom", [])

        # Combine default + custom strategies for the multiselect options
        all_options = DEFAULT_STRATEGIES + [
            s for s in custom_strats if s not in DEFAULT_STRATEGIES
        ]

        # ---- Multiselect for strategy choices ----
        selected_now = st.multiselect(
            "Which strategies do you plan to use?",
            options=all_options,
            default=selected_existing,
            key="strategies_selected",
        )

        # ---- Add custom strategies ----
        st.markdown("###### Add your own strategy")
        st.caption(
            "Have a strategy that works for you (e.g., ‘record myself explaining and play it back’)? "
            "Add it here and it will appear in the list above."
        )

        new_strategy = st.text_input(
            "Type a new strategy",
            key="new_strategy_text",
            placeholder="e.g., Study in 15-minute sprints with music off",
        )

        if st.button("➕ Add custom strategy", key="add_custom_strategy"):
            cleaned = new_strategy.strip()
            if not cleaned:
                st.warning("Please type a strategy before adding it.")
            else:
                if cleaned in all_options:
                    st.info("That strategy is already in your list.")
                else:
                    custom_strats.append(cleaned)
                    # Include the new strategy as selected
                    updated_selected = selected_now + [cleaned]
                    update_current_session(
                        {
                            "strategies": {
                                "selected": updated_selected,
                                "custom": custom_strats,
                            }
                        }
                    )
                    st.success("Custom strategy added and selected ✅")

                    # Mark for clearing on the next rerun
                    st.session_state["clear_new_strategy_input"] = True

                    # Keep local variables in sync for this render
                    selected_now = updated_selected
                    all_options.append(cleaned)

        # ---- Save the current set of selected strategies ----
        if st.button("Save strategies", key="save_strategies"):
            update_current_session(
                {
                    "strategies": {
                        "selected": selected_now,
                        "custom": custom_strats,
                    }
                }
            )
            st.success("Strategies saved 💡")

        # ---- Quick summary of chosen strategies ----
        if selected_now:
            st.markdown("##### Your chosen strategies for this task")
            for s_item in selected_now:
                st.markdown(f"- {s_item}")

        st.markdown("---")
        st.markdown("##### Ask AI for strategy ideas")

        msg = st.text_area(
            "Describe your situation (time available, task type, how you like to study), "
            "and the assistant will suggest strategies.",
            key="strategies_ai_input",
            height=150,
        )

        if st.button("✨ Suggest strategies", key="strategies_ai_button") and msg.strip():
            # Use the safe AI wrapper to generate strategy suggestions with caching and rate limiting
            with st.spinner("Thinking about strategies that might fit..."):
                reply = safe_ai(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])


