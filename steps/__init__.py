# steps/__init__.py
from importlib import import_module

REGISTRY = {}

def _register(mod_name: str, cls_name: str):
    """Import steps.<mod_name> and register its Step class if present."""
    try:
        mod = import_module(f".{mod_name}", __name__)
        cls = getattr(mod, cls_name)
        key = getattr(cls, "key", mod_name)
        REGISTRY[key] = cls()
    except Exception as e:
        # Don’t crash the whole app if one step fails
        print(f"[steps] Skipped {mod_name}: {e}")

# List of (module filename, class name) pairs
for mod_name, cls_name in [
    ("goals", "GoalsStep"),
    ("task_analysis", "TaskAnalysisStep"),
    ("strategies", "StrategiesStep"),
    ("time_plan", "TimePlanStep"),
    ("resources", "ResourcesStep"),
    ("reflection", "ReflectionStep"),
    ("feedback", "FeedbackStep"),
    # ("save_session", "SaveStep"),  # optional
]:
    _register(mod_name, cls_name)
