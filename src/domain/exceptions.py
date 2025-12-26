"""Custom exceptions for the Todo domain."""


class TodoError(Exception):
    """Base exception for Todo application errors."""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with the specified ID does not exist."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")


class ValidationError(TodoError):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
