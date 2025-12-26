# Research: Phase I – In-Memory CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Date**: 2025-12-26
**Status**: Complete

## Technical Decisions

### Decision 1: Programming Language

**Decision**: Python 3.11+

**Rationale**:
- Rapid development for CLI applications
- Built-in argument parsing (argparse)
- Strong typing support (type hints) for domain clarity
- Cross-platform compatibility (Linux, macOS, Windows)
- Enum support for status representation
- Excellent for Phase I focus on correctness over performance

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| TypeScript/Node | Type safety, npm ecosystem | Requires Node runtime, async complexity | Overkill for in-memory CLI |
| Go | Fast compilation, single binary | More verbose for simple domain logic | Unnecessary complexity |
| Rust | Memory safety, performance | Steep learning curve, slow iteration | Premature optimization |

### Decision 2: Task ID Strategy

**Decision**: Auto-increment integer starting at 1

**Rationale**:
- Simpler and more deterministic than UUIDs
- Human-readable for CLI interaction
- Easy to track "next available ID"
- Aligns with spec requirement: "Task IDs MUST be positive integers, incrementing from 1"

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| UUID | Globally unique, no collision | Not human-readable, harder to type | Violates spec (positive integers) |
| Random integer | Unique | Not deterministic, harder to debug | Violates determinism principle |

### Decision 3: Data Storage Structure

**Decision**: Dictionary (dict) keyed by task ID

**Rationale**:
- O(1) lookup by ID for all operations
- Clear semantics: ID → Task mapping
- Natural fit for create, read, update, delete operations
- Maintains insertion order (Python 3.7+)

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| List | Simple iteration | O(n) lookup by ID | Poor performance for lookups |
| OrderedDict | Explicit ordering | Redundant in Python 3.7+ | Unnecessary complexity |

### Decision 4: Status Representation

**Decision**: Explicit enum with values `pending` and `completed`

**Rationale**:
- Type safety prevents invalid states
- Self-documenting code
- Future extensibility (can add `archived`, `in_progress` etc.)
- Clear mapping to spec status values

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Boolean (completed: true/false) | Simpler | Less extensible, less readable | Limits future phases |
| String literals | Flexible | No type safety, typo risk | Error-prone |

### Decision 5: Error Reporting Strategy

**Decision**: Explicit user-facing error messages to stderr

**Rationale**:
- Debuggability for users and judges
- Follows FR-019 through FR-022 (error handling requirements)
- Separates errors (stderr) from results (stdout)
- Non-zero exit codes for scripting compatibility

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Silent failures | Simpler code | Violates FR-019, impossible to debug | Spec violation |
| Exceptions only | Pythonic | Requires try/catch, poor UX | Not user-friendly |

### Decision 6: CLI Framework

**Decision**: Python argparse (standard library)

**Rationale**:
- Zero external dependencies (spec constraint: no external dependencies)
- Built-in help generation
- Subcommand support for operations (add, list, update, complete, delete)
- Sufficient for Phase I requirements

**Alternatives Considered**:
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Click | Cleaner API, decorators | External dependency | Violates constraint |
| Typer | Type hints integration | External dependency | Violates constraint |
| sys.argv manual | No dependencies | Poor UX, no help | Insufficient features |

### Decision 7: Architecture Layers

**Decision**: Three-layer separation (Domain → Application → Interface)

**Rationale**:
- Domain layer: Task entity, state transitions, validation rules
- Application layer: Use cases (create, list, update, complete, delete)
- Interface layer: CLI parsing and output formatting
- Clean separation enables future phases (Web API, AI chatbot)
- Aligns with constitution principle: "Pure domain logic separated from CLI I/O"

**Layer Responsibilities**:

| Layer | Responsibility | Dependencies |
|-------|----------------|--------------|
| Domain | Task entity, TaskStatus enum, validation | None |
| Application | TaskManager (use cases), ID generation | Domain |
| Interface | CLI parsing, output formatting, error display | Application |

## Testing Strategy

**Decision**: Manual CLI testing against acceptance scenarios

**Rationale**:
- Phase I focuses on correctness validation via spec
- 18 acceptance scenarios provide comprehensive coverage
- No automated test framework adds complexity
- Judges can validate by running CLI commands

**Test Categories**:
1. **Happy path**: Each user story's primary flow
2. **Edge cases**: Empty titles, long titles, special characters
3. **Error cases**: Non-existent IDs, invalid input
4. **Idempotency**: Repeated operations produce consistent results

## Unresolved Items

None. All technical decisions are resolved based on user input and spec requirements.

## References

- Spec: `specs/001-cli-todo/spec.md`
- Constitution: `.specify/memory/constitution.md`
- Phase I Governance: "Core domain logic MUST be correct and testable"
