# steps/__init__.py
from .goals import GoalsStep
from .task_analysis import TaskAnalysisStep
from .strategies import StrategiesStep
from .time_plan import TimePlanStep
from .resources import ResourcesStep
from .reflection import ReflectionStep
from .feedback import FeedbackStep
# optional:
# from .save_session import SaveStep

REGISTRY = {
    GoalsStep.key: GoalsStep(),
    TaskAnalysisStep.key: TaskAnalysisStep(),
    StrategiesStep.key: StrategiesStep(),
    TimePlanStep.key: TimePlanStep(),
    ResourcesStep.key: ResourcesStep(),
    ReflectionStep.key: ReflectionStep(),
    FeedbackStep.key: FeedbackStep(),
    # "save": SaveStep(),
}
