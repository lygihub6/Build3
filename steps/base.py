"""
Abstract base class for SRL steps.

Each self‑regulated learning module (step) in the app should inherit
from ``BaseStep`` and implement the ``render`` method to display its
UI using Streamlit components. The class attributes ``id``, ``label``,
``emoji`` and ``description`` should be set by subclasses to define
how the step appears in the module selector.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseStep(ABC):
    """Abstract base class defining the interface for a SRL step."""

    id: str  # internal identifier (e.g. "goal", "task")
    label: str  # display name (e.g. "Goal Setting")
    emoji: str  # emoji used in module selector
    description: str  # one‑sentence description for the sidebar

    @abstractmethod
    def render(self, session: Dict[str, Any]) -> None:
        """
        Render the UI for this step.

        Each subclass must implement this method to draw its specific
        widgets and handle user interactions. The current session
        dictionary is passed in for context.
        """
        raise NotImplementedError

    def call_ai(self, user_message: str, session: Dict[str, Any]) -> str:
        """
        Call the AI assistant safely for this step.

        This convenience method wraps the ``safe_ai`` helper from ``services.ai``.
        It automatically passes the step's ``id`` along with the user message
        and current session into ``safe_ai`` to obtain a model response.
        The ``safe_ai`` function caches responses and throttles API calls to
        avoid exceeding rate limits.

        Args:
            user_message: The input text to send to the AI.
            session: The current session dictionary providing context.

        Returns:
            A string containing the AI-generated reply, a cached response, or
            a throttle warning if requests are too frequent.
        """
        # Local import to avoid circular dependencies at module load time.
        from services.ai import safe_ai  # type: ignore

        return safe_ai(self.id, user_message, session)