# state.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class SRLState:
    current_step: str = "goals"
    messages: List[Dict[str, str]] = field(default_factory=list)
    learning_goals: List[str] = field(default_factory=list)
    task_info: str = ""
    strategies: List[str] = field(default_factory=list)
    time_plan: str = ""
    resources: List[str] = field(default_factory=list)
    reflections: List[str] = field(default_factory=list)
    saved_sessions: List[Dict[str, Any]] = field(default_factory=list)
    session_start: datetime = field(default_factory=datetime.now)
    timer_running: bool = False
    timer_start: Optional[float] = None
    timer_duration_min: int = 25

def get_state(st):
    if "srl" not in st.session_state:
        st.session_state.srl = SRLState()
    return st.session_state.srl
