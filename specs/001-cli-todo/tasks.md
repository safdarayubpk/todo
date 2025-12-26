# Tasks: Phase I – In-Memory CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-interface.md

**Tests**: Manual CLI testing against acceptance scenarios (no automated tests requested)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Project type**: Single project (CLI application)
- **Domain**: `src/domain/`
- **Application**: `src/application/`
- **CLI**: `src/cli/`

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/domain/, src/application/, src/cli/
- [x] T002 [P] Create src/domain/__init__.py with module docstring
- [x] T003 [P] Create src/application/__init__.py with module docstring
- [x] T004 [P] Create src/cli/__init__.py with module docstring

**Checkpoint**: Project structure ready for domain implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core domain entities that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Implement TaskStatus enum (pending, completed) in src/domain/task.py
- [x] T006 Implement Task entity with id, title, description, status in src/domain/task.py
- [x] T007 Add Task validation: non-empty title, max 500 chars in src/domain/task.py
- [x] T008 Implement TaskList aggregate with tasks dict and next_id in src/domain/task_list.py
- [x] T009 Add TaskList.get(id) method returning Task or None in src/domain/task_list.py
- [x] T010 Implement custom exceptions (TaskNotFoundError, ValidationError) in src/domain/exceptions.py
- [x] T011 [P] Create src/domain/exceptions.py with TaskNotFoundError, ValidationError classes

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Create and List Tasks (Priority: P1)

**Goal**: Users can create tasks and see all their tasks

**Independent Test**: Create multiple tasks, list them, verify IDs and status

### Implementation for User Story 1

- [x] T012 [US1] Implement TaskList.create(title, description) in src/domain/task_list.py
- [x] T013 [US1] Implement TaskList.list() returning all tasks in src/domain/task_list.py
- [x] T014 [US1] Create TaskManager class with task_list instance in src/application/task_manager.py
- [x] T015 [US1] Implement TaskManager.create_task(title, description) in src/application/task_manager.py
- [x] T016 [US1] Implement TaskManager.list_tasks() in src/application/task_manager.py
- [x] T017 [US1] Create output formatter for task list display in src/cli/formatters.py
- [x] T018 [US1] Implement format_task_list() with ID, Status, Title columns in src/cli/formatters.py
- [x] T019 [US1] Implement format_empty_list() message in src/cli/formatters.py
- [x] T020 [US1] Create CLI entry point with argparse in src/cli/main.py
- [x] T021 [US1] Implement 'add' command handler in src/cli/commands.py
- [x] T022 [US1] Implement 'list' command handler in src/cli/commands.py
- [x] T023 [US1] Wire add and list commands to main.py argument parser in src/cli/main.py
- [x] T024 [US1] Add error output to stderr with exit code 1 in src/cli/main.py

**Checkpoint**: User Story 1 complete - can create and list tasks independently

**Manual Validation** (US1 Acceptance Scenarios):
```bash
# Scenario 1: Create task with title only
python3 src/cli/main.py add "Buy groceries"
# Expected: Created task 1: Buy groceries

# Scenario 2: Create task with description
python3 src/cli/main.py add "Call mom" --description "Wish her happy birthday"
# Expected: Created task 2: Call mom

# Scenario 3: List tasks
python3 src/cli/main.py list
# Expected: Table with tasks 1 and 2, status [ ]

# Scenario 4: List empty (restart app)
python3 src/cli/main.py list
# Expected: No tasks found.

# Scenario 5: Unique IDs
python3 src/cli/main.py add "Task A"
python3 src/cli/main.py add "Task B"
# Expected: Different IDs (1, 2)
```

---

## Phase 4: User Story 2 - Complete Tasks (Priority: P2)

**Goal**: Users can mark tasks as complete or reopen them

**Independent Test**: Create task, complete it, verify status change, uncomplete it

### Implementation for User Story 2

- [x] T025 [US2] Implement TaskList.complete(id) in src/domain/task_list.py
- [x] T026 [US2] Implement TaskList.uncomplete(id) in src/domain/task_list.py
- [x] T027 [US2] Add idempotent behavior for complete/uncomplete in src/domain/task_list.py
- [x] T028 [US2] Implement TaskManager.complete_task(id) in src/application/task_manager.py
- [x] T029 [US2] Implement TaskManager.uncomplete_task(id) in src/application/task_manager.py
- [x] T030 [US2] Implement format_complete_result() in src/cli/formatters.py
- [x] T031 [US2] Implement format_uncomplete_result() in src/cli/formatters.py
- [x] T032 [US2] Implement 'complete' command handler in src/cli/commands.py
- [x] T033 [US2] Implement 'uncomplete' command handler in src/cli/commands.py
- [x] T034 [US2] Wire complete and uncomplete commands to main.py in src/cli/main.py

**Checkpoint**: User Story 2 complete - can complete and uncomplete tasks

**Manual Validation** (US2 Acceptance Scenarios):
```bash
# Setup: Create a task first
python3 src/cli/main.py add "Test task"

# Scenario 1: Complete pending task
python3 src/cli/main.py complete 1
# Expected: Completed task 1: Test task

# Scenario 2: Complete already completed (idempotent)
python3 src/cli/main.py complete 1
# Expected: Task 1 is already completed: Test task

# Scenario 3: Uncomplete completed task
python3 src/cli/main.py uncomplete 1
# Expected: Reopened task 1: Test task

# Scenario 4: Uncomplete already pending (idempotent)
python3 src/cli/main.py uncomplete 1
# Expected: Task 1 is already pending: Test task

# Scenario 5: Complete non-existent task
python3 src/cli/main.py complete 999
# Expected: Error: Task 999 not found (exit 1)
```

---

## Phase 5: User Story 3 - Update Tasks (Priority: P3)

**Goal**: Users can update task title and description

**Independent Test**: Create task, update title, verify change, update description

### Implementation for User Story 3

- [x] T035 [US3] Implement TaskList.update(id, title, description) in src/domain/task_list.py
- [x] T036 [US3] Add validation for non-empty title on update in src/domain/task_list.py
- [x] T037 [US3] Ensure update preserves task status in src/domain/task_list.py
- [x] T038 [US3] Implement TaskManager.update_task(id, title, description) in src/application/task_manager.py
- [x] T039 [US3] Implement format_update_result() in src/cli/formatters.py
- [x] T040 [US3] Implement 'update' command handler with --title and --description in src/cli/commands.py
- [x] T041 [US3] Wire update command to main.py argument parser in src/cli/main.py
- [x] T042 [US3] Add validation error for no changes specified in src/cli/commands.py

**Checkpoint**: User Story 3 complete - can update task details

**Manual Validation** (US3 Acceptance Scenarios):
```bash
# Setup: Create a task
python3 src/cli/main.py add "Buy grocries"

# Scenario 1: Update title
python3 src/cli/main.py update 1 --title "Buy groceries"
# Expected: Updated task 1: Buy groceries

# Scenario 2: Add description
python3 src/cli/main.py update 1 --description "From the farmer's market"
# Expected: Updated task 1: Buy groceries

# Scenario 3: Update preserves status
python3 src/cli/main.py complete 1
python3 src/cli/main.py update 1 --title "Shopping"
python3 src/cli/main.py list
# Expected: Task 1 still shows [x] (completed)

# Scenario 4: Update non-existent
python3 src/cli/main.py update 999 --title "New"
# Expected: Error: Task 999 not found (exit 1)

# Scenario 5: Update with empty title
python3 src/cli/main.py update 1 --title ""
# Expected: Error: Task title cannot be empty (exit 1)
```

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Create tasks, delete one, verify removal, check ID not reused

### Implementation for User Story 4

- [x] T043 [US4] Implement TaskList.delete(id) in src/domain/task_list.py
- [x] T044 [US4] Ensure deleted IDs are never reused in src/domain/task_list.py
- [x] T045 [US4] Implement TaskManager.delete_task(id) in src/application/task_manager.py
- [x] T046 [US4] Implement format_delete_result() in src/cli/formatters.py
- [x] T047 [US4] Implement 'delete' command handler in src/cli/commands.py
- [x] T048 [US4] Wire delete command to main.py argument parser in src/cli/main.py

**Checkpoint**: User Story 4 complete - all CRUD operations functional

**Manual Validation** (US4 Acceptance Scenarios):
```bash
# Setup: Create tasks
python3 src/cli/main.py add "Task A"
python3 src/cli/main.py add "Task B"

# Scenario 1: Delete task
python3 src/cli/main.py delete 1
# Expected: Deleted task 1: Task A

# Scenario 2: Delete non-existent
python3 src/cli/main.py delete 999
# Expected: Error: Task 999 not found (exit 1)

# Scenario 3: ID not reused
python3 src/cli/main.py add "Task C"
python3 src/cli/main.py list
# Expected: Task C has ID 3 (not 1)

# Scenario 4: Other tasks unchanged
python3 src/cli/main.py list
# Expected: Task B (ID 2) still present
```

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [x] T049 Add --help and --version global options in src/cli/main.py
- [x] T050 Implement help text matching cli-interface.md contract in src/cli/main.py
- [x] T051 Add input validation for non-integer IDs in src/cli/commands.py
- [x] T052 Verify all error messages match contracts/cli-interface.md in src/cli/commands.py
- [x] T053 Run full acceptance scenario validation (18 scenarios)
- [x] T054 Verify deterministic behavior (same inputs = same outputs)

---

## Dependencies & Execution Order

### Phase Dependencies

```text
Phase 1 (Setup) ─────────────────────────────────────────┐
                                                          │
Phase 2 (Foundational) ◄──────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────────────────────────┐
│ User Stories can proceed in parallel after Foundational   │
│ OR sequentially in priority order (P1 → P2 → P3 → P4)     │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  Phase 3 (US1: Create/List) ─┬─► Phase 4 (US2: Complete)  │
│           │                  │                            │
│           │                  ├─► Phase 5 (US3: Update)    │
│           │                  │                            │
│           │                  └─► Phase 6 (US4: Delete)    │
│           │                                               │
│           └──► US2, US3, US4 depend on US1 for setup      │
│                                                           │
└───────────────────────────────────────────────────────────┘
                          │
                          ▼
                Phase 7 (Polish)
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Create/List) | Foundational | Phase 2 complete |
| US2 (Complete) | US1 | Phase 3 complete |
| US3 (Update) | US1 | Phase 3 complete |
| US4 (Delete) | US1 | Phase 3 complete |

### Within Each Phase

1. Domain layer tasks first (task_list.py methods)
2. Application layer tasks second (task_manager.py)
3. CLI layer tasks last (commands.py, formatters.py, main.py)

---

## Parallel Opportunities

### Phase 1 (Setup)
```bash
# All init files can be created in parallel:
T002, T003, T004  # [P] markers
```

### Phase 2 (Foundational)
```bash
# After T005-T009, exceptions can be created in parallel:
T011  # [P] marker - independent file
```

### After Phase 3 (US1 Complete)
```bash
# US2, US3, US4 domain tasks can proceed in parallel:
Phase 4: T025-T027 (domain)
Phase 5: T035-T037 (domain)
Phase 6: T043-T044 (domain)
# Then application, then CLI layers sequentially within each story
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T011)
3. Complete Phase 3: User Story 1 (T012-T024)
4. **STOP and VALIDATE**: Run US1 acceptance scenarios
5. Deploy/demo if ready - you have a working task creator!

### Incremental Delivery

| Milestone | Tasks | Deliverable |
|-----------|-------|-------------|
| Foundation | T001-T011 | Project structure, domain entities |
| MVP | T012-T024 | Create and list tasks |
| Completion | T025-T034 | Complete/uncomplete tasks |
| Update | T035-T042 | Update task details |
| Delete | T043-T048 | Delete tasks |
| Polish | T049-T054 | Help, validation, final check |

---

## Task Summary

| Phase | Story | Task Count | Parallel Tasks |
|-------|-------|------------|----------------|
| Setup | - | 4 | 3 |
| Foundational | - | 7 | 1 |
| US1 | Create/List | 13 | 0 |
| US2 | Complete | 10 | 0 |
| US3 | Update | 8 | 0 |
| US4 | Delete | 6 | 0 |
| Polish | - | 6 | 0 |
| **Total** | | **54** | **4** |

---

## Notes

- [P] tasks = different files, no dependencies
- [USn] label maps task to specific user story
- Each user story is independently testable after completion
- Manual validation scripts provided for each story
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
