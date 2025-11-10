# steps/base.py
from typing import Protocol
import streamlit as st
from state import SRLState

class StepModule(Protocol):
    key: str
    label: str
    icon: str

    def render(self, st: "streamlit", state: SRLState) -> None: ...
