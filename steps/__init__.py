"""
Register all SRL steps in a central list.

This module imports each concrete ``BaseStep`` subclass and constructs
an ordered list called ``STEPS``. The application iterates over this
list to render the module selector and to locate the active step. A
helper function ``get_step_by_id`` returns the step instance for a
given identifier.
"""

from __future__ import annotations

from typing import List, Optional

# Import each step class. If you add a new step, import it here and
# append an instance to the STEPS list.
from .tutorial import TutorialStep
from .goals import GoalsStep
from .task_analysis import TaskAnalysisStep
from .strategies import StrategiesStep
from .time_plan import TimePlanStep
from .resources import ResourcesStep
from .reflection import ReflectionStep
from .feedback import FeedbackStep


# Ordered list of all available steps. The order determines how
# they appear in the module selector on the left.
STEPS: List[BaseStep] = [
    TutorialStep(),
    GoalsStep(),
    TaskAnalysisStep(),
    StrategiesStep(),
    TimePlanStep(),
    ResourcesStep(),
    ReflectionStep(),
    FeedbackStep(),
]


def get_step_by_id(step_id: str) -> Optional[BaseStep]:
    """Return the step instance with the matching identifier.

    Args:
        step_id: the identifier of the step to retrieve.

    Returns:
        The corresponding step instance, or ``None`` if not found.
    """
    for step in STEPS:
        if step.id == step_id:
            return step
    return None
