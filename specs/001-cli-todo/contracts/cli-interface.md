# CLI Interface Contract: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Date**: 2025-12-26
**Source**: `specs/001-cli-todo/spec.md`

## Command Overview

| Command | Description | Exit Code (Success) | Exit Code (Error) |
|---------|-------------|---------------------|-------------------|
| `add` | Create a new task | 0 | 1 |
| `list` | Display all tasks | 0 | 1 |
| `update` | Modify task title/description | 0 | 1 |
| `complete` | Mark task as completed | 0 | 1 |
| `uncomplete` | Mark task as pending | 0 | 1 |
| `delete` | Remove a task | 0 | 1 |

## Command Specifications

### `add` - Create Task

**Usage**:
```bash
todo add <title> [--description <text>]
todo add "Buy groceries"
todo add "Call mom" --description "Wish her happy birthday"
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `title` | string | Yes | Task title (non-empty, max 500 chars) |
| `--description`, `-d` | string | No | Optional task description |

**Output (stdout)**:
```text
Created task 1: Buy groceries
```

**Errors (stderr)**:
| Condition | Message | Exit Code |
|-----------|---------|-----------|
| Empty title | Error: Task title cannot be empty | 1 |
| Title too long | Error: Task title exceeds 500 characters | 1 |

---

### `list` - List All Tasks

**Usage**:
```bash
todo list
```

**Arguments**: None

**Output (stdout)** - Tasks exist:
```text
ID  Status     Title
--  ------     -----
1   [ ]        Buy groceries
2   [x]        Call mom
3   [ ]        Submit report
```

**Output (stdout)** - No tasks:
```text
No tasks found.
```

**Status Indicators**:
| Status | Display |
|--------|---------|
| pending | `[ ]` |
| completed | `[x]` |

---

### `update` - Update Task

**Usage**:
```bash
todo update <id> [--title <text>] [--description <text>]
todo update 1 --title "Buy organic groceries"
todo update 1 --description "From farmer's market"
todo update 1 --title "Shopping" --description "Weekly groceries"
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to update |
| `--title`, `-t` | string | No | New title (non-empty if provided) |
| `--description`, `-d` | string | No | New description (empty allowed) |

**Output (stdout)**:
```text
Updated task 1: Buy organic groceries
```

**Errors (stderr)**:
| Condition | Message | Exit Code |
|-----------|---------|-----------|
| Task not found | Error: Task 999 not found | 1 |
| Empty title | Error: Task title cannot be empty | 1 |
| Invalid ID | Error: Invalid task ID | 1 |
| No changes | Error: No changes specified | 1 |

---

### `complete` - Mark Task Complete

**Usage**:
```bash
todo complete <id>
todo complete 1
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to complete |

**Output (stdout)**:
```text
Completed task 1: Buy groceries
```

**Output (stdout)** - Already completed (idempotent):
```text
Task 1 is already completed: Buy groceries
```

**Errors (stderr)**:
| Condition | Message | Exit Code |
|-----------|---------|-----------|
| Task not found | Error: Task 999 not found | 1 |
| Invalid ID | Error: Invalid task ID | 1 |

---

### `uncomplete` - Mark Task Pending

**Usage**:
```bash
todo uncomplete <id>
todo uncomplete 1
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to mark pending |

**Output (stdout)**:
```text
Reopened task 1: Buy groceries
```

**Output (stdout)** - Already pending (idempotent):
```text
Task 1 is already pending: Buy groceries
```

**Errors (stderr)**:
| Condition | Message | Exit Code |
|-----------|---------|-----------|
| Task not found | Error: Task 999 not found | 1 |
| Invalid ID | Error: Invalid task ID | 1 |

---

### `delete` - Delete Task

**Usage**:
```bash
todo delete <id>
todo delete 1
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | integer | Yes | Task ID to delete |

**Output (stdout)**:
```text
Deleted task 1: Buy groceries
```

**Errors (stderr)**:
| Condition | Message | Exit Code |
|-----------|---------|-----------|
| Task not found | Error: Task 999 not found | 1 |
| Invalid ID | Error: Invalid task ID | 1 |

---

## Global Options

| Option | Description |
|--------|-------------|
| `--help`, `-h` | Display help for command |
| `--version`, `-v` | Display application version |

**Help Output**:
```text
todo - In-Memory CLI Todo Application

Usage: todo <command> [options]

Commands:
  add         Create a new task
  list        Display all tasks
  update      Modify task title/description
  complete    Mark task as completed
  uncomplete  Mark task as pending
  delete      Remove a task

Options:
  -h, --help     Show this help message
  -v, --version  Show version number

Examples:
  todo add "Buy groceries"
  todo add "Call mom" -d "Wish her happy birthday"
  todo list
  todo complete 1
  todo update 1 --title "Buy organic groceries"
  todo delete 1
```

## I/O Conventions

| Stream | Content |
|--------|---------|
| stdin | Not used (all input via arguments) |
| stdout | Success messages, task listings |
| stderr | Error messages |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Operation completed successfully |
| 1 | Operation failed (see stderr for details) |

## Character Handling

- All text is UTF-8 encoded
- Special characters in titles/descriptions are preserved
- Quotes in arguments follow shell escaping rules
- Newlines in descriptions are preserved
