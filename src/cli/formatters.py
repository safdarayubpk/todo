"""Output formatters for CLI display."""

from typing import List

from src.domain.task import Task, TaskStatus


def format_task_list(tasks: List[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: List of tasks to format.

    Returns:
        Formatted string with ID, Status, and Title columns.
    """
    if not tasks:
        return format_empty_list()

    lines = [
        "ID  Status     Title",
        "--  ------     -----"
    ]

    for task in tasks:
        status_indicator = "[x]" if task.status == TaskStatus.COMPLETED else "[ ]"
        lines.append(f"{task.id:<3} {status_indicator:<10} {task.title}")

    return "\n".join(lines)


def format_empty_list() -> str:
    """Format message for empty task list.

    Returns:
        Message indicating no tasks exist.
    """
    return "No tasks found."


def format_create_result(task: Task) -> str:
    """Format the result of creating a task.

    Args:
        task: The created task.

    Returns:
        Success message with task ID and title.
    """
    return f"Created task {task.id}: {task.title}"


def format_complete_result(task: Task, was_changed: bool) -> str:
    """Format the result of completing a task.

    Args:
        task: The task that was completed.
        was_changed: Whether the status actually changed.

    Returns:
        Message indicating completion or already completed.
    """
    if was_changed:
        return f"Completed task {task.id}: {task.title}"
    return f"Task {task.id} is already completed: {task.title}"


def format_uncomplete_result(task: Task, was_changed: bool) -> str:
    """Format the result of uncompleting a task.

    Args:
        task: The task that was reopened.
        was_changed: Whether the status actually changed.

    Returns:
        Message indicating reopening or already pending.
    """
    if was_changed:
        return f"Reopened task {task.id}: {task.title}"
    return f"Task {task.id} is already pending: {task.title}"


def format_update_result(task: Task) -> str:
    """Format the result of updating a task.

    Args:
        task: The updated task.

    Returns:
        Success message with task ID and new title.
    """
    return f"Updated task {task.id}: {task.title}"


def format_delete_result(task: Task) -> str:
    """Format the result of deleting a task.

    Args:
        task: The deleted task.

    Returns:
        Success message with task ID and title.
    """
    return f"Deleted task {task.id}: {task.title}"
