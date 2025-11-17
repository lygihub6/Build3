
from typing import Dict, Any

import streamlit as st

from steps.base import Step
from state import update_current_session
from services.ai import call_gemini_for_module


class ResourcesStep(Step):
    def __init__(self):
        super().__init__(id="resources", title="Resources", icon="📚")

    def render(self, session: Dict[str, Any]):
        self.show_header()
        st.markdown("List the key resources you will actually use for this task.")

        res_name = st.text_input(
            "Resource name or short description",
            key="res_name",
            placeholder="e.g., Chapter 5: Climate Systems (textbook)",
        )

        res_type = st.selectbox(
            "Type",
            [
                "",
                "Textbook / reading",
                "Academic article",
                "Video / tutorial",
                "Tool / software",
                "Person / tutor / office hours",
                "Other",
            ],
            key="res_type",
        )

        res_link = st.text_input(
            "Link or location (optional)",
            key="res_link",
            placeholder="https://... or 'Library, shelf QC 903'",
        )

        if st.button("➕ Add resource", key="add_resource"):
            if not res_name.strip():
                st.warning("Give the resource at least a short name.")
            else:
                resources = list(session.get("resources", []))
                resources.append({"name": res_name.strip(), "type": res_type.strip(), "link": res_link.strip()})
                update_current_session({"resources": resources})
                st.success("Resource added.")
                st.session_state["res_name"] = ""
                st.session_state["res_type"] = ""
                st.session_state["res_link"] = ""

        resources = session.get("resources", [])
        if resources:
            st.markdown("##### Your resources")
            for r in resources:
                line = f"- **{r.get('name','(no name)')}**"
                if r.get("type"):
                    line += f"  ·  {r['type']}"
                if r.get("link"):
                    line += f"  ·  {r['link']}"
                st.markdown(line)

        st.markdown("---")
        st.markdown("##### Ask AI for resource ideas")

        msg = st.text_area(
            "Describe what kind of explanations, examples, or tools help you most, and the assistant can suggest resource types.",
            key="resources_ai_input",
            height=120,
        )

        if st.button("🔎 Suggest resources", key="resources_ai_button") and msg.strip():
            with st.spinner("Looking for resource ideas..."):
                reply = call_gemini_for_module("resources", msg, session)
            st.session_state["ai_responses"]["resources"] = reply

        if st.session_state["ai_responses"].get("resources"):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"]["resources"])
