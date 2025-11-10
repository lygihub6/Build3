# steps/strategies.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

STRATEGY_BANK = [
    "Elaboration (explain in your own words, connect to examples)",
    "Practice testing (self-quizzes, flashcards with retrieval)",
    "Spaced repetition (review over days, not crammed)",
    "Worked examples → faded example problems",
    "Note-taking with cues (Cornell / outline + questions)",
    "Teach-back (explain to a peer or rubber duck)",
    "Dual coding (words + diagram/timeline/flow)",
    "Error log: track mistakes and fix patterns",
]

class StrategiesStep(StepModule):
    key, label, icon = "strategies", "Strategies", "🧠"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Plan Learning Strategies")

        st.markdown("Pick a few strategies aligned to your goals & task.")
        chosen = st.multiselect("Suggested strategies", STRATEGY_BANK)

        custom = st.text_area("Add custom strategies (one per line)", height=120)

        if st.button("Save Strategies"):
            strategies = chosen[:]
            if custom.strip():
                strategies += [s.strip() for s in custom.splitlines() if s.strip()]
            if strategies:
                state.strategies = strategies
                st.success(f"Saved {len(strategies)} strategy(ies).")
                st.rerun()

        if state.strategies:
            st.markdown("---")
            st.markdown("**Your Strategy Plan**")
            for i, s in enumerate(state.strategies, 1):
                st.write(f"{i}. {s}")
