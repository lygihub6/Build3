# steps/resources.py
import streamlit as st
from steps.base import StepModule
from state import SRLState

TYPES = ["Textbook/Chapter", "Video/Lecture", "Practice/Problem set", "Examples/Solutions", "Peer/TA", "Office hours/Forum"]

class ResourcesStep(StepModule):
    key, label, icon = "resources", "Resources", "📚"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Identify Resources")

        entries = []
        for i in range(1, 4):
            st.markdown(f"**Resource {i}**")
            r_type = st.selectbox(f"Type {i}", TYPES, key=f"r_type_{i}")
            desc = st.text_input(f"Description/Link {i}", key=f"r_desc_{i}")
            why  = st.text_input(f"Why helpful {i}", key=f"r_why_{i}")
            if desc.strip():
                entries.append(f"{r_type}: {desc} — {why}")

        if st.button("Save Resources"):
            if entries:
                state.resources = entries
                st.success(f"Saved {len(entries)} resource(s).")
                st.rerun()

        if state.resources:
            st.markdown("---")
            st.markdown("**Planned Resources**")
            for i, r in enumerate(state.resources, 1):
                st.write(f"{i}. {r}")
