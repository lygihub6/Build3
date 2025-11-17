
from abc import ABC, abstractmethod
from typing import Dict, Any

import streamlit as st


class Step(ABC):
    """Base class for all SRL steps/modules."""

    id: str
    title: str
    icon: str

    def __init__(self, id: str, title: str, icon: str):
        self.id = id
        self.title = title
        self.icon = icon

    @abstractmethod
    def render(self, session: Dict[str, Any]):
        ...

    def show_header(self):
        st.subheader(f"{self.icon} {self.title}")
