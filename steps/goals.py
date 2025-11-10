# steps/goals.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

class GoalsStep(StepModule):
    key, label, icon = "goals", "Goals", "🎯"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Set Mastery Goals")
        g = st.text_area("What will you be able to **know/do** by the end? (1–2 goals)")
        c1,c2 = st.columns([1,1])
        with c1:
            if st.button("Add Goal"):
                if g.strip():
                    state.learning_goals.append(g.strip())
                    st.success("Goal added.")
                    st.rerun()
        with c2:
            if st.button("Clear Goals"):
                state.learning_goals.clear()
                st.rerun()
        if state.learning_goals:
            st.markdown("**Your goals:**")
            for i,goal in enumerate(state.learning_goals,1):
                st.write(f"{i}. {goal}")
