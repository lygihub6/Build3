# steps/reflection.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

class ReflectionStep(StepModule):
    key, label, icon = "reflection", "Reflection", "🤔"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Reflect")
        prompts = [
            "What went well?",
            "What was hard and why?",
            "Which strategy helped most?",
            "What will you change next time?"
        ]
        ans = [st.text_area(p) for p in prompts]
        if st.button("Save Reflection"):
            text = "\n".join([f"- {p} {a}" for p,a in zip(prompts, ans) if a.strip()])
            if text:
                state.reflections.append(text)
                st.success("Saved.")
                st.rerun()
        if state.reflections:
            st.markdown("---")
            st.markdown("**Recent reflections**")
            for r in state.reflections[-3:]:
                st.info(r)
