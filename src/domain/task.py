"""Task entity and TaskStatus enum for the Todo domain."""

from enum import Enum
from typing import Optional

from .exceptions import ValidationError


class TaskStatus(Enum):
    """Represents the completion state of a task."""
    PENDING = "pending"
    COMPLETED = "completed"


class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique, immutable, positive integer identifier assigned by system.
        title: Non-empty string describing the task (required).
        description: Optional string providing additional details.
        status: Current completion state (pending or completed).
    """

    MAX_TITLE_LENGTH = 500

    def __init__(
        self,
        task_id: int,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING
    ):
        """Initialize a Task.

        Args:
            task_id: Unique positive integer identifier.
            title: Non-empty task title.
            description: Optional task description.
            status: Task status (defaults to PENDING).

        Raises:
            ValidationError: If title is empty or exceeds max length.
        """
        self._validate_title(title)
        self._id = task_id
        self._title = title
        self._description = description
        self._status = status

    @staticmethod
    def _validate_title(title: str) -> None:
        """Validate task title.

        Args:
            title: The title to validate.

        Raises:
            ValidationError: If title is empty, whitespace-only, or too long.
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")
        if len(title) > Task.MAX_TITLE_LENGTH:
            raise ValidationError(f"Task title exceeds {Task.MAX_TITLE_LENGTH} characters")

    @property
    def id(self) -> int:
        """Get the task ID (immutable)."""
        return self._id

    @property
    def title(self) -> str:
        """Get the task title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set the task title.

        Args:
            value: New title value.

        Raises:
            ValidationError: If title is empty or too long.
        """
        self._validate_title(value)
        self._title = value

    @property
    def description(self) -> Optional[str]:
        """Get the task description."""
        return self._description

    @description.setter
    def description(self, value: Optional[str]) -> None:
        """Set the task description."""
        self._description = value

    @property
    def status(self) -> TaskStatus:
        """Get the task status."""
        return self._status

    @status.setter
    def status(self, value: TaskStatus) -> None:
        """Set the task status."""
        self._status = value

    def __repr__(self) -> str:
        """Return string representation of the task."""
        return (
            f"Task(id={self._id}, title={self._title!r}, "
            f"description={self._description!r}, status={self._status.value})"
        )
