# Implementation Plan: Phase I – In-Memory CLI Todo Application

**Branch**: `001-cli-todo` | **Date**: 2025-12-26 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-cli-todo/spec.md`

## Summary

Build an in-memory CLI todo application that establishes the core domain model for the
Evolution of Todo system. The application provides CRUD operations for tasks via command
line, with all data stored in memory. This phase focuses on correctness, determinism,
and clean separation between domain logic and CLI interface.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (standard library only: argparse, enum)
**Storage**: In-memory dictionary keyed by task ID
**Testing**: Manual CLI testing against 18 acceptance scenarios
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single project (CLI application)
**Performance Goals**: <1s for task creation, <2s for listing 1000 tasks
**Constraints**: No external dependencies, no persistence, single-process
**Scale/Scope**: Single user, unlimited tasks (memory-bound)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Specification Supremacy

| Check | Status | Evidence |
|-------|--------|----------|
| Feature maps to spec artifact | PASS | `specs/001-cli-todo/spec.md` |
| Spec defines purpose, scope, constraints | PASS | Overview, Constraints, Out of Scope sections |
| Acceptance criteria defined | PASS | 18 scenarios across 4 user stories |

### Principle II: Phase Continuity

| Check | Status | Evidence |
|-------|--------|----------|
| Valid evolutionary step | PASS | Phase I is the foundation |
| Backward compatibility addressed | N/A | First phase |
| Technology aligns with phase | PASS | CLI-only, no web/AI/K8s |

### Principle III: Determinism First

| Check | Status | Evidence |
|-------|--------|----------|
| State transitions explicit | PASS | `data-model.md` state diagram |
| No hidden logic/side effects | PASS | All operations documented |
| Behavior traceable | PASS | Every command maps to spec |

### Principle IV: User-Centric Correctness

| Check | Status | Evidence |
|-------|--------|----------|
| Error handling deliberate | PASS | FR-019 to FR-022, error table in contracts |
| Acceptance criteria pass | PENDING | Implementation not started |
| Behavior spec-traceable | PASS | All 26 FRs map to operations |

### Principle V: Isolation by Design

| Check | Status | Evidence |
|-------|--------|----------|
| User data isolated | PASS | Single-user, single-process |
| No cross-user access | N/A | Single user |
| No hardcoded secrets | PASS | No auth in Phase I |

### Principle VI: AI as Executor

| Check | Status | Evidence |
|-------|--------|----------|
| AI within defined capabilities | PASS | Following spec-driven workflow |
| Spec defines truth | PASS | spec.md is authoritative |
| Workflow followed | PASS | Constitution → Spec → Plan → Tasks |

### Principle VII: Observability

| Check | Status | Evidence |
|-------|--------|----------|
| Behavior explainable | PASS | CLI output is human-readable |
| State transitions traceable | PASS | stdout/stderr separation |
| Infrastructure specified | PASS | No infrastructure needed |

**Gate Status**: PASS - All applicable principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technical decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
├── contracts/           # Interface contracts
│   └── cli-interface.md # CLI command specifications
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── domain/
│   ├── __init__.py
│   ├── task.py          # Task entity, TaskStatus enum
│   └── task_list.py     # TaskList aggregate, ID management
├── application/
│   ├── __init__.py
│   └── task_manager.py  # Use cases: create, list, update, complete, delete
└── cli/
    ├── __init__.py
    ├── main.py          # Entry point, argument parsing
    ├── commands.py      # Command handlers
    └── formatters.py    # Output formatting

tests/
└── manual/
    └── acceptance.md    # Manual test scripts for 18 scenarios
```

**Structure Decision**: Single project with three-layer architecture (Domain → Application → CLI).
This separation enables future phases to add Web API or AI interfaces without modifying domain logic.

## Architecture Decisions

### ADR-001: Three-Layer Architecture

**Context**: Need clean separation for future phase evolution.

**Decision**: Implement Domain, Application, and Interface layers.

**Consequences**:
- Domain layer has no dependencies on Application or Interface
- Application layer depends only on Domain
- CLI layer depends on Application (never directly on Domain internals)
- Future Web API can reuse Application layer

### ADR-002: Dictionary-Based Storage

**Context**: Need efficient task lookup by ID.

**Decision**: Use Python dict keyed by task ID.

**Consequences**:
- O(1) lookup, insert, delete operations
- Natural fit for CRUD operations
- Maintains insertion order (Python 3.7+)

### ADR-003: Enum for Task Status

**Context**: Need type-safe status representation.

**Decision**: Use Python Enum with values `pending` and `completed`.

**Consequences**:
- Type safety prevents invalid states
- Extensible for future phases (could add `archived`, `in_progress`)
- Self-documenting code

### ADR-004: No External Dependencies

**Context**: Spec requires application runs without external dependencies.

**Decision**: Use only Python standard library (argparse, enum).

**Consequences**:
- Zero installation friction
- Guaranteed compatibility
- Simpler testing and deployment

## Complexity Tracking

> No Constitution Check violations requiring justification.

| Item | Complexity | Justification |
|------|------------|---------------|
| Three layers | Low | Standard separation, enables future phases |
| Enum for status | Low | Type safety, extensibility |
| Dict storage | Low | Optimal for CRUD by ID |

## Phase 0 Artifacts

- [x] `research.md` - Technical decisions documented

## Phase 1 Artifacts

- [x] `data-model.md` - Entity definitions
- [x] `contracts/cli-interface.md` - CLI command specifications
- [x] `quickstart.md` - Usage guide

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement Domain layer first (Task, TaskStatus, TaskList)
3. Implement Application layer (TaskManager)
4. Implement CLI layer (main.py, commands, formatters)
5. Validate against 18 acceptance scenarios
