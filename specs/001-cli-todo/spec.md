# Feature Specification: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Created**: 2025-12-26
**Status**: Draft
**Phase**: Phase I of Evolution of Todo
**Input**: In-Memory CLI Todo Application with deterministic domain logic

## Overview

This specification defines the foundational phase of the Evolution of Todo system: a command-line
todo application that operates entirely in memory. This phase establishes the core domain model
and behavioral rules that all future phases will build upon.

**Target Users**:
- Individual users managing personal tasks via command-line interface
- Judges evaluating correctness, spec adherence, and domain modeling

**Primary Focus**:
- Correctness and determinism of core Todo domain logic
- Establishing a stable behavioral foundation for future phases

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create and List Tasks (Priority: P1)

As a user, I want to create todo tasks and see all my tasks so that I can track what I need to do.

**Why this priority**: This is the core functionality - without creating and viewing tasks, the
application has no value. This story alone delivers a minimal viable product.

**Independent Test**: Can be fully tested by creating tasks and listing them. Delivers immediate
value as a basic task tracker.

**Acceptance Scenarios**:

1. **Given** an empty task list, **When** user creates a task with title "Buy groceries",
   **Then** the task is created with a unique ID, status "pending", and the provided title.

2. **Given** an empty task list, **When** user creates a task with title "Call mom" and
   description "Wish her happy birthday", **Then** the task is created with the title,
   description, unique ID, and status "pending".

3. **Given** one or more tasks exist, **When** user lists all tasks, **Then** all tasks are
   displayed with their ID, title, and status indicator.

4. **Given** an empty task list, **When** user lists all tasks, **Then** the system displays
   a message indicating no tasks exist.

5. **Given** a task was created, **When** user creates another task, **Then** the new task
   receives a different unique ID that has never been used.

---

### User Story 2 - Complete Tasks (Priority: P2)

As a user, I want to mark tasks as complete so that I can track my progress and see what
I have accomplished.

**Why this priority**: Completion is the natural progression after creating tasks. Users need
to mark progress to get value from the task list.

**Independent Test**: Requires P1 (create/list) to set up tasks, then can independently test
completion behavior.

**Acceptance Scenarios**:

1. **Given** a task exists with status "pending", **When** user marks it as complete,
   **Then** the task status changes to "completed".

2. **Given** a task exists with status "completed", **When** user marks it as complete again,
   **Then** the task remains "completed" with no error (idempotent operation).

3. **Given** a task exists with status "completed", **When** user marks it as incomplete,
   **Then** the task status changes to "pending".

4. **Given** a task exists with status "pending", **When** user marks it as incomplete,
   **Then** the task remains "pending" with no error (idempotent operation).

5. **Given** no task exists with ID "999", **When** user attempts to complete task "999",
   **Then** the system displays a clear error message indicating the task was not found.

---

### User Story 3 - Update Tasks (Priority: P3)

As a user, I want to update task details so that I can correct mistakes or add more information
without recreating the task.

**Why this priority**: Updates are important but less critical than creation and completion.
Users can work around missing updates by deleting and recreating tasks.

**Independent Test**: Requires P1 (create/list) to set up tasks, then can independently test
update behavior.

**Acceptance Scenarios**:

1. **Given** a task exists with title "Buy grocries", **When** user updates the title to
   "Buy groceries", **Then** the task title is updated and all other attributes remain unchanged.

2. **Given** a task exists without a description, **When** user adds description "From the
   farmer's market", **Then** the task has the new description and all other attributes
   remain unchanged.

3. **Given** a task exists with status "completed", **When** user updates the title,
   **Then** the title is updated and the status remains "completed".

4. **Given** no task exists with ID "999", **When** user attempts to update task "999",
   **Then** the system displays a clear error message indicating the task was not found.

5. **Given** a task exists, **When** user attempts to update with an empty title,
   **Then** the system rejects the update with a clear error message, and the task
   remains unchanged.

---

### User Story 4 - Delete Tasks (Priority: P4)

As a user, I want to delete tasks so that I can remove items that are no longer relevant
and keep my task list clean.

**Why this priority**: Deletion is useful for maintenance but not essential for core
task tracking workflow.

**Independent Test**: Requires P1 (create/list) to set up tasks, then can independently test
deletion behavior.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "1", **When** user deletes task "1", **Then** the task
   is permanently removed and no longer appears in the task list.

2. **Given** no task exists with ID "999", **When** user attempts to delete task "999",
   **Then** the system displays a clear error message indicating the task was not found.

3. **Given** a task with ID "1" was deleted, **When** user creates a new task, **Then**
   the new task receives a new unique ID (ID "1" is never reused).

4. **Given** multiple tasks exist, **When** user deletes one task, **Then** all other
   tasks remain unchanged.

---

### Edge Cases

- **Empty title**: Creating or updating a task with an empty or whitespace-only title
  MUST be rejected with a clear error message.
- **Very long title**: Titles up to 500 characters MUST be accepted.
- **Special characters**: Titles and descriptions containing special characters, unicode,
  and newlines MUST be handled correctly.
- **ID format**: Task IDs MUST be positive integers, incrementing from 1.
- **Concurrent operations**: Not applicable (single-user, single-process constraint).
- **Maximum tasks**: No artificial limit; bounded only by available memory.

## Requirements *(mandatory)*

### Functional Requirements

**Task Creation**:
- **FR-001**: System MUST allow creating a task with a non-empty title
- **FR-002**: System MUST allow creating a task with an optional description
- **FR-003**: System MUST assign a unique, immutable, positive integer ID to each new task
- **FR-004**: System MUST set initial task status to "pending" on creation
- **FR-005**: System MUST never reuse task IDs, even after deletion

**Task Listing**:
- **FR-006**: System MUST display all tasks with their ID, title, and status
- **FR-007**: System MUST indicate when the task list is empty
- **FR-008**: System MUST show task descriptions when available

**Task Completion**:
- **FR-009**: System MUST allow marking a pending task as completed
- **FR-010**: System MUST allow marking a completed task as pending (toggle back)
- **FR-011**: System MUST handle re-completing an already completed task without error
- **FR-012**: System MUST handle marking an already pending task as pending without error

**Task Update**:
- **FR-013**: System MUST allow updating a task's title (non-empty required)
- **FR-014**: System MUST allow updating a task's description (empty allowed)
- **FR-015**: System MUST preserve task status when updating other fields
- **FR-016**: System MUST preserve task ID when updating any field

**Task Deletion**:
- **FR-017**: System MUST allow permanent deletion of a task by ID
- **FR-018**: System MUST remove deleted tasks from all listings

**Error Handling**:
- **FR-019**: System MUST return clear error for operations on non-existent task IDs
- **FR-020**: System MUST return clear error for empty or invalid titles
- **FR-021**: System MUST NOT crash on invalid input
- **FR-022**: System MUST NOT allow partial state changes on failure

**Interface**:
- **FR-023**: System MUST provide command-line interface for all operations
- **FR-024**: System MUST accept input via command arguments and/or stdin
- **FR-025**: System MUST output results to stdout
- **FR-026**: System MUST output errors to stderr

### Key Entities

- **Task**: Represents a single todo item
  - `id`: Unique, immutable, positive integer identifier assigned by system
  - `title`: Non-empty string describing the task (required)
  - `description`: Optional string providing additional details
  - `status`: Current state, one of: `pending` | `completed`

- **TaskList**: In-memory collection of all tasks
  - Contains zero or more Task entities
  - Maintains ID uniqueness and ordering
  - Tracks next available ID (never decrements)

## Constraints

- **Interface**: Command-line only (no GUI, no web server)
- **Storage**: In-memory only (no files, no databases)
- **Execution**: Single-user, single-process
- **Architecture**: Pure domain logic separated from CLI I/O
- **Development**: Spec-driven (no manual coding outside workflow)

## Assumptions

- Task IDs start at 1 and increment sequentially
- All operations complete synchronously
- Application state is lost when process exits (by design for Phase I)
- Character encoding is UTF-8
- No maximum task limit is enforced (memory-bound only)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a task in under 1 second response time
- **SC-002**: Users can list 1000 tasks in under 2 seconds response time
- **SC-003**: 100% of acceptance scenarios pass without manual intervention
- **SC-004**: All operations produce identical results when repeated with same inputs
  (determinism)
- **SC-005**: Zero crashes occur when processing invalid input
- **SC-006**: Judges can validate all behavior by reading this specification alone
- **SC-007**: All task state transitions follow the defined rules exactly

## Out of Scope

The following are explicitly NOT part of this specification:

- Persistent storage (files, databases)
- User authentication or multi-user support
- Due dates, priorities, tags, or reminders
- AI, NLP, or chatbot interfaces
- Concurrency or background processing
- Logging, metrics, or observability tooling
- Search or filtering functionality
- Sorting or ordering options
- Bulk operations
