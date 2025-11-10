# steps/__init__.py
from .goals import GoalsStep
from .reflection import ReflectionStep
# from .task_analysis import TaskAnalysisStep
# from .strategies import StrategiesStep
# from .time_plan import TimePlanStep
# from .resources import ResourcesStep
# from .feedback import FeedbackStep

REGISTRY = {
    GoalsStep.key: GoalsStep(),
    ReflectionStep.key: ReflectionStep(),
    # "task_analysis": TaskAnalysisStep(),
    # "strategies": StrategiesStep(),
    # "time_plan": TimePlanStep(),
    # "resources": ResourcesStep(),
    # "feedback": FeedbackStep(),
}
