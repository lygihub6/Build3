"""
Resources step implementation.

Students can record the books, articles, videos, tools, people, and
other resources they intend to use for their tasks. The module also
provides an AI assistant to suggest categories of resources to
consider. Resources are stored in the current session’s ``resources``
list.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from state import update_current_session
from services.ai import call_gemini_for_module
from .base import BaseStep


class ResourcesStep(BaseStep):
    """Resources SRL step."""

    id = "resources"
    label = "Resources"
    emoji = "📚"
    description = "Identify and organize the materials you need."

    def render(self, session: Dict[str, Any]) -> None:
        # Clear resource inputs on the next run after a successful add
        if st.session_state.get("clear_resource_inputs"):
            for key in ("res_name", "res_type", "res_link"):
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state["clear_resource_inputs"] = False

        st.subheader("📚 Resources")
        st.markdown("List the key resources you will actually use for this task.")

        # Input widgets for adding a resource
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
                resources.append(
                    {
                        "name": res_name.strip(),
                        "type": res_type.strip(),
                        "link": res_link.strip(),
                    }
                )
                update_current_session({"resources": resources})
                st.success("Resource added.")

                # Tell the next rerun to clear the inputs *before* widgets are built
                st.session_state["clear_resource_inputs"] = True

        # Display the list of resources
        resources = session.get("resources", [])
        if resources:
            st.markdown("##### Your resources")
            for r in resources:
                line = f"- **{r.get('name', '(no name)')}**"
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
                reply = call_gemini_for_module(self.id, msg, session)
            st.session_state.setdefault("ai_responses", {})[self.id] = reply

        if st.session_state.get("ai_responses", {}).get(self.id):
            st.markdown("###### AI suggestion")
            st.markdown(st.session_state["ai_responses"][self.id])
