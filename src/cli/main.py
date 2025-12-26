#!/usr/bin/env python3
"""CLI entry point for the Todo application."""

import argparse
import sys

from src.application.task_manager import TaskManager
from src.cli.commands import (
    handle_add,
    handle_list,
    handle_complete,
    handle_uncomplete,
    handle_update,
    handle_delete,
    parse_task_id,
)

__version__ = "1.0.0"

# Global TaskManager instance (in-memory, lost on exit)
_manager = TaskManager()


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="todo - In-Memory CLI Todo Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  todo add "Buy groceries"
  todo add "Call mom" -d "Wish her happy birthday"
  todo list
  todo complete 1
  todo update 1 --title "Buy organic groceries"
  todo delete 1
"""
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Create a new task")
    add_parser.add_argument("title", help="Task title (non-empty, max 500 chars)")
    add_parser.add_argument(
        "-d", "--description",
        help="Optional task description"
    )

    # List command
    subparsers.add_parser("list", help="Display all tasks")

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as completed")
    complete_parser.add_argument("id", help="Task ID to complete")

    # Uncomplete command
    uncomplete_parser = subparsers.add_parser("uncomplete", help="Mark task as pending")
    uncomplete_parser.add_argument("id", help="Task ID to mark pending")

    # Update command
    update_parser = subparsers.add_parser("update", help="Modify task title/description")
    update_parser.add_argument("id", help="Task ID to update")
    update_parser.add_argument(
        "-t", "--title",
        help="New title (non-empty if provided)"
    )
    update_parser.add_argument(
        "-d", "--description",
        help="New description (empty allowed)"
    )

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Remove a task")
    delete_parser.add_argument("id", help="Task ID to delete")

    return parser


def main() -> int:
    """Main entry point.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "add":
        return handle_add(_manager, args.title, args.description)

    elif args.command == "list":
        return handle_list(_manager)

    elif args.command == "complete":
        try:
            task_id = parse_task_id(args.id)
            return handle_complete(_manager, task_id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "uncomplete":
        try:
            task_id = parse_task_id(args.id)
            return handle_uncomplete(_manager, task_id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "update":
        try:
            task_id = parse_task_id(args.id)
            return handle_update(_manager, task_id, args.title, args.description)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif args.command == "delete":
        try:
            task_id = parse_task_id(args.id)
            return handle_delete(_manager, task_id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
