"""Command handlers for CLI operations."""

import sys
from typing import Optional

from src.application.task_manager import TaskManager
from src.domain.exceptions import TaskNotFoundError, ValidationError
from src.cli.formatters import (
    format_task_list,
    format_create_result,
    format_complete_result,
    format_uncomplete_result,
    format_update_result,
    format_delete_result,
)


def handle_add(manager: TaskManager, title: str, description: Optional[str] = None) -> int:
    """Handle the 'add' command.

    Args:
        manager: The TaskManager instance.
        title: Task title.
        description: Optional task description.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = manager.create_task(title, description)
        print(format_create_result(task))
        return 0
    except ValidationError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_list(manager: TaskManager) -> int:
    """Handle the 'list' command.

    Args:
        manager: The TaskManager instance.

    Returns:
        Exit code (0 for success).
    """
    tasks = manager.list_tasks()
    print(format_task_list(tasks))
    return 0


def handle_complete(manager: TaskManager, task_id: int) -> int:
    """Handle the 'complete' command.

    Args:
        manager: The TaskManager instance.
        task_id: ID of the task to complete.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task, was_changed = manager.complete_task(task_id)
        print(format_complete_result(task, was_changed))
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_uncomplete(manager: TaskManager, task_id: int) -> int:
    """Handle the 'uncomplete' command.

    Args:
        manager: The TaskManager instance.
        task_id: ID of the task to uncomplete.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task, was_changed = manager.uncomplete_task(task_id)
        print(format_uncomplete_result(task, was_changed))
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_update(
    manager: TaskManager,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> int:
    """Handle the 'update' command.

    Args:
        manager: The TaskManager instance.
        task_id: ID of the task to update.
        title: New title (optional).
        description: New description (optional).

    Returns:
        Exit code (0 for success, 1 for error).
    """
    if title is None and description is None:
        print("Error: No changes specified", file=sys.stderr)
        return 1

    try:
        task = manager.update_task(task_id, title, description)
        print(format_update_result(task))
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValidationError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_delete(manager: TaskManager, task_id: int) -> int:
    """Handle the 'delete' command.

    Args:
        manager: The TaskManager instance.
        task_id: ID of the task to delete.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = manager.delete_task(task_id)
        print(format_delete_result(task))
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def parse_task_id(id_str: str) -> int:
    """Parse and validate a task ID from string.

    Args:
        id_str: The string representation of the task ID.

    Returns:
        The parsed task ID as an integer.

    Raises:
        ValueError: If the ID is not a valid positive integer.
    """
    try:
        task_id = int(id_str)
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        return task_id
    except ValueError:
        raise ValueError("Invalid task ID")
