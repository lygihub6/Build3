
from .goals import GoalsStep
from .task_analysis import TaskAnalysisStep
from .strategies import StrategiesStep
from .time_plan import TimePlanStep
from .resources import ResourcesStep
from .reflection import ReflectionStep
from .feedback import FeedbackStep


STEPS = [
    GoalsStep(),
    TaskAnalysisStep(),
    StrategiesStep(),
    TimePlanStep(),
    ResourcesStep(),
    ReflectionStep(),
    FeedbackStep(),
]


def get_step_by_id(step_id: str):
    for step in STEPS:
        if step.id == step_id:
            return step
    return STEPS[0]
