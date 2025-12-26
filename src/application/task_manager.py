"""TaskManager - Application layer use cases for task management."""

from typing import List, Optional

from src.domain.task import Task
from src.domain.task_list import TaskList
from src.domain.exceptions import TaskNotFoundError, ValidationError


class TaskManager:
    """Manages task operations and coordinates domain logic.

    This class provides the application-level use cases for task management,
    delegating to the domain layer for business rules.
    """

    def __init__(self):
        """Initialize TaskManager with an empty TaskList."""
        self._task_list = TaskList()

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task.

        Args:
            title: Non-empty task title.
            description: Optional task description.

        Returns:
            The newly created Task.

        Raises:
            ValidationError: If title is invalid.
        """
        return self._task_list.create(title, description)

    def list_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks.
        """
        return self._task_list.list()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        return self._task_list.get(task_id)

    def complete_task(self, task_id: int) -> tuple[Task, bool]:
        """Mark a task as completed.

        Args:
            task_id: The ID of the task to complete.

        Returns:
            Tuple of (task, was_changed).

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        return self._task_list.complete(task_id)

    def uncomplete_task(self, task_id: int) -> tuple[Task, bool]:
        """Mark a task as pending.

        Args:
            task_id: The ID of the task to mark pending.

        Returns:
            Tuple of (task, was_changed).

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        return self._task_list.uncomplete(task_id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (must be non-empty if provided).
            description: New description.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task doesn't exist.
            ValidationError: If title is invalid.
        """
        return self._task_list.update(task_id, title, description)

    def delete_task(self, task_id: int) -> Task:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted Task.

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        return self._task_list.delete(task_id)
