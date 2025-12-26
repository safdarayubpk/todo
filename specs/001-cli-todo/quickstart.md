# Quickstart: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Date**: 2025-12-26

## Prerequisites

- Python 3.11 or higher
- No external dependencies required

## Installation

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd todo

# Verify Python version
python3 --version  # Should show 3.11+

# Make the CLI executable (optional)
chmod +x src/cli/main.py
```

## Running the Application

```bash
# Using Python directly
python3 src/cli/main.py <command> [options]

# Or with the alias (if configured)
todo <command> [options]
```

## Basic Usage

### Create Tasks

```bash
# Create a simple task
python3 src/cli/main.py add "Buy groceries"
# Output: Created task 1: Buy groceries

# Create a task with description
python3 src/cli/main.py add "Call mom" --description "Wish her happy birthday"
# Output: Created task 2: Call mom
```

### List Tasks

```bash
python3 src/cli/main.py list
# Output:
# ID  Status     Title
# --  ------     -----
# 1   [ ]        Buy groceries
# 2   [ ]        Call mom
```

### Complete a Task

```bash
python3 src/cli/main.py complete 1
# Output: Completed task 1: Buy groceries

python3 src/cli/main.py list
# Output:
# ID  Status     Title
# --  ------     -----
# 1   [x]        Buy groceries
# 2   [ ]        Call mom
```

### Reopen a Task

```bash
python3 src/cli/main.py uncomplete 1
# Output: Reopened task 1: Buy groceries
```

### Update a Task

```bash
python3 src/cli/main.py update 1 --title "Buy organic groceries"
# Output: Updated task 1: Buy organic groceries

python3 src/cli/main.py update 2 --description "Sunday afternoon"
# Output: Updated task 2: Call mom
```

### Delete a Task

```bash
python3 src/cli/main.py delete 1
# Output: Deleted task 1: Buy organic groceries
```

## Verification Checklist

Run these commands to verify the application works correctly:

### Test 1: Create and List

```bash
# Start fresh (restart application)
python3 src/cli/main.py add "Test task"
python3 src/cli/main.py list
# Expected: Task 1 with status [ ] and title "Test task"
```

### Test 2: Complete and Uncomplete

```bash
python3 src/cli/main.py complete 1
python3 src/cli/main.py list
# Expected: Task 1 with status [x]

python3 src/cli/main.py uncomplete 1
python3 src/cli/main.py list
# Expected: Task 1 with status [ ]
```

### Test 3: Error Handling

```bash
python3 src/cli/main.py complete 999
# Expected: Error message on stderr, exit code 1

python3 src/cli/main.py add ""
# Expected: Error message about empty title

python3 src/cli/main.py add "  "
# Expected: Error message about empty title (whitespace-only)
```

### Test 4: ID Uniqueness

```bash
python3 src/cli/main.py add "Task A"  # Gets ID 1
python3 src/cli/main.py add "Task B"  # Gets ID 2
python3 src/cli/main.py delete 1
python3 src/cli/main.py add "Task C"  # Gets ID 3 (not 1!)
python3 src/cli/main.py list
# Expected: Tasks 2 and 3 only, ID 1 is not reused
```

## Notes

- **In-Memory Storage**: All tasks are lost when the application exits. This is by design for Phase I.
- **Single Process**: The application is meant to be run in a single process. Each run starts with an empty task list.
- **No Persistence**: Do not expect tasks to survive between runs.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `python3: command not found` | Install Python 3.11+ or use `python` instead |
| `Permission denied` | Run `chmod +x src/cli/main.py` |
| Tasks disappear between runs | This is expected (in-memory storage) |
| Unicode characters display wrong | Ensure terminal supports UTF-8 |

## Next Steps

After verifying the quickstart:

1. Review acceptance scenarios in `specs/001-cli-todo/spec.md`
2. Run through all 18 acceptance scenarios manually
3. Verify error handling for edge cases
4. Confirm deterministic behavior (same inputs = same outputs)
