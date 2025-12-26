# Data Model: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Date**: 2025-12-26
**Source**: `specs/001-cli-todo/spec.md`

## Entities

### TaskStatus (Enum)

Represents the completion state of a task.

| Value | Description |
|-------|-------------|
| `pending` | Task is not yet completed (default state) |
| `completed` | Task has been marked as done |

**Constraints**:
- Only these two values are valid
- Default value on task creation: `pending`
- Transitions: `pending` ↔ `completed` (bidirectional)

### Task (Entity)

Represents a single todo item.

| Field | Type | Required | Mutable | Description |
|-------|------|----------|---------|-------------|
| `id` | positive integer | Yes | No | Unique identifier assigned by system |
| `title` | non-empty string | Yes | Yes | Brief description of the task |
| `description` | string or null | No | Yes | Optional detailed description |
| `status` | TaskStatus | Yes | Yes | Current completion state |

**Validation Rules**:

| Field | Rule | Error Message |
|-------|------|---------------|
| `id` | Must be positive integer | "Task ID must be a positive integer" |
| `id` | Must be unique | "Task ID {id} already exists" |
| `title` | Must not be empty or whitespace-only | "Task title cannot be empty" |
| `title` | Maximum 500 characters | "Task title exceeds maximum length" |
| `description` | No validation (null or any string) | N/A |
| `status` | Must be valid TaskStatus value | "Invalid task status" |

**Invariants**:
- ID is assigned at creation and never changes
- ID is never reused after deletion
- Status can only be `pending` or `completed`

### TaskList (Aggregate)

In-memory collection managing all tasks.

| Property | Type | Description |
|----------|------|-------------|
| `tasks` | dict[int, Task] | Map of task ID to Task entity |
| `next_id` | positive integer | Next available ID (starts at 1, never decrements) |

**Operations**:

| Operation | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| `create` | title, description? | Task | Increments next_id, adds to tasks |
| `list` | none | list[Task] | None |
| `get` | id | Task or None | None |
| `update` | id, title?, description? | Task | Modifies task in place |
| `complete` | id | Task | Sets status to completed |
| `uncomplete` | id | Task | Sets status to pending |
| `delete` | id | bool | Removes from tasks |

**Invariants**:
- `next_id` only increases (never decreases, even after deletion)
- `tasks` keys are always valid positive integers
- No duplicate IDs exist in `tasks`

## State Transitions

### Task Lifecycle

```text
[Create] → pending → [Complete] → completed
                ↑                      ↓
                └──── [Uncomplete] ────┘

[Delete] removes task from any state
```

### State Transition Rules

| Current State | Action | New State | Side Effects |
|---------------|--------|-----------|--------------|
| (new) | create | pending | ID assigned, added to TaskList |
| pending | complete | completed | Status updated |
| pending | uncomplete | pending | No change (idempotent) |
| completed | complete | completed | No change (idempotent) |
| completed | uncomplete | pending | Status updated |
| any | update | same | Title/description updated, status preserved |
| any | delete | (removed) | Task removed from TaskList |

## Error Conditions

| Condition | Triggered By | Error Type |
|-----------|--------------|------------|
| Task not found | get/update/complete/delete with invalid ID | NotFoundError |
| Empty title | create/update with empty string | ValidationError |
| Title too long | create/update with >500 chars | ValidationError |
| Invalid ID format | non-integer ID in any operation | ValidationError |

## Data Examples

### Valid Task

```text
Task {
  id: 1,
  title: "Buy groceries",
  description: "Milk, bread, eggs",
  status: pending
}
```

### Minimal Task

```text
Task {
  id: 2,
  title: "Call mom",
  description: null,
  status: pending
}
```

### Completed Task

```text
Task {
  id: 3,
  title: "Submit report",
  description: "Q4 financial summary",
  status: completed
}
```

## Relationships

```text
┌─────────────┐         ┌──────────────┐
│  TaskList   │ 1────*  │    Task      │
├─────────────┤         ├──────────────┤
│ tasks       │────────→│ id           │
│ next_id     │         │ title        │
└─────────────┘         │ description  │
                        │ status ──────┼──→ TaskStatus
                        └──────────────┘
```

## Notes

- No persistence: all data is lost when application exits
- No timestamps: created_at, updated_at are out of scope for Phase I
- No ordering: tasks are stored by ID, no explicit sort order
- No relationships between tasks (no subtasks, dependencies)
