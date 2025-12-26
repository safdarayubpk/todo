"""TaskList aggregate for managing the in-memory collection of tasks."""

from typing import Dict, List, Optional

from .task import Task, TaskStatus
from .exceptions import TaskNotFoundError, ValidationError


class TaskList:
    """In-memory collection managing all tasks.

    Attributes:
        tasks: Dictionary mapping task ID to Task entity.
        next_id: Next available ID (starts at 1, never decrements).
    """

    def __init__(self):
        """Initialize an empty TaskList."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def get(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def create(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task.

        Args:
            title: Non-empty task title.
            description: Optional task description.

        Returns:
            The newly created Task.

        Raises:
            ValidationError: If title is invalid.
        """
        task = Task(
            task_id=self._next_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def list(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks in creation order.
        """
        return list(self._tasks.values())

    def complete(self, task_id: int) -> tuple[Task, bool]:
        """Mark a task as completed.

        Args:
            task_id: The ID of the task to complete.

        Returns:
            Tuple of (task, was_changed) where was_changed is False if already completed.

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        was_changed = task.status != TaskStatus.COMPLETED
        task.status = TaskStatus.COMPLETED
        return task, was_changed

    def uncomplete(self, task_id: int) -> tuple[Task, bool]:
        """Mark a task as pending.

        Args:
            task_id: The ID of the task to mark pending.

        Returns:
            Tuple of (task, was_changed) where was_changed is False if already pending.

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        was_changed = task.status != TaskStatus.PENDING
        task.status = TaskStatus.PENDING
        return task, was_changed

    def update(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (must be non-empty if provided).
            description: New description (can be empty string or None).

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task doesn't exist.
            ValidationError: If title is empty or too long.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        if title is not None:
            task.title = title  # Validation happens in setter

        if description is not None:
            task.description = description

        return task

    def delete(self, task_id: int) -> Task:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted Task.

        Raises:
            TaskNotFoundError: If task doesn't exist.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        # Note: next_id is NOT decremented to ensure IDs are never reused
        return task

    def __len__(self) -> int:
        """Return the number of tasks."""
        return len(self._tasks)
