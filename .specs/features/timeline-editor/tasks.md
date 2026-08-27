# Timeline Editor Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `tlc-spec-driven` skill: activate it by name and follow its Execute flow and Critical Rules. Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, gate, atomic commit, Verifier, and discrimination sensor).

**Design**: `.specs/features/timeline-editor/design.md`
**Status**: In Progress

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec - confirm before Execute. Guidelines found: none - strong defaults applied; user confirmed pytest unit and integration tests plus manual UI acceptance.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Domain model | unit | All branches; 1:1 to CARD and LINK acceptance criteria; all listed deletion and invalid-reference edge cases | `tests/test_model.py` | `python -m pytest` |
| JSON repository | integration | Save/load happy path, empty project, malformed/incompatible input, and failed-load state preservation | `tests/test_storage.py` | `python -m pytest` |
| Desktop UI | none | Manual acceptance is documented separately; no automated GUI test framework is required for the MVP | `docs/manual-acceptance.md` | `python -m time_spock` |
| Configuration and entry point | none | Build gate only | `pyproject.toml`, `src/time_spock/main.py` | `python -m compileall src` |

## Gate Check Commands

> Generated from the empty repository and confirmed test strategy.

| Gate Level | When to Use | Command |
| --- | --- | --- |
| Quick | After model or storage tasks | `python -m pytest` |
| Full | After UI integration | `python -m pytest; python -m compileall src` |
| Build | After configuration or final phase | `python -m compileall src; python -m pytest` |

## Execution Plan

Phases are ordered and run sequentially. Tasks within a phase execute in the listed order.

### Phase 1: Foundation

```text
T1
```

### Phase 2: Core Data

```text
T1 -> T2 -> T3
```

### Phase 3: Desktop Editor

```text
T3 -> T4 -> T5 -> T6 -> T7
```

## Task Breakdown

### T1: Create Python project configuration

**What**: Add the minimal package metadata, dependency declaration, pytest configuration, and application entry-point metadata needed to run the project.
**Where**: `pyproject.toml`
**Depends on**: None
**Reuses**: None; repository is empty.
**Requirement**: Project foundation for all requirements.

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] `pyproject.toml` declares Python, PySide6, and pytest dependencies.
- [x] The package entry point is `time_spock.main:main`.
- [x] Build gate passes: `C:/Users/fabio/AppData/Local/Programs/Python/Python310/python.exe -c "from setuptools.config.pyprojecttoml import read_configuration; read_configuration('pyproject.toml')"`.

**Tests**: none
**Gate**: build
**Commit**: `build(timeline-editor): configure python desktop project`

### T2: Implement the project domain model

**What**: Implement cards, timelines, memberships, directed connections, validation, and deletion behavior in the project model.
**Where**: `src/time_spock/model.py`
**Depends on**: T1
**Reuses**: Dataclasses and UUID generation from the Python standard library.
**Requirement**: CARD-01..06, LINK-01..04, LANE-01, LANE-03..05

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Cards, timelines, memberships, and connections have stable identifiers and serializable fields.
- [x] Card title validation, directed branching, shared memberships, and connection validation match the specification.
- [x] Card deletion removes only related memberships and connections.
- [x] `tests/test_model.py` covers every applicable model acceptance criterion and listed model edge case.
- [x] Quick gate passes: `python -m pytest`.

**Tests**: unit
**Gate**: quick
**Commit**: `feat(timeline-editor): add project domain model`

### T3: Implement JSON project persistence

**What**: Add versioned JSON save/load with complete project serialization and validation before replacing active state.
**Where**: `src/time_spock/storage.py`
**Depends on**: T2
**Reuses**: `Project` model and Python `json` and `pathlib` modules.
**Requirement**: FILE-01..05 and empty-project edge case

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] Save writes cards, timelines, memberships, positions, connections, and schema version.
- [x] Load reconstructs a valid project with the same values and relationships.
- [x] Malformed, missing, or incompatible files raise a controlled application error before active state replacement.
- [x] `tests/test_storage.py` covers round-trip, empty project, malformed input, incompatible input, and failed-load preservation.
- [x] Quick gate passes: `python -m pytest`.

**Tests**: integration
**Gate**: quick
**Commit**: `feat(timeline-editor): add json project persistence`

### T4: Implement the graphics scene

**What**: Add the `QGraphicsScene` editor surface with timeline regions, movable card instances, directed connection rendering, selection, and scene signals.
**Where**: `src/time_spock/ui/scene.py`
**Depends on**: T3
**Reuses**: `Project`, `Membership`, `Connection`, `QGraphicsScene`, and `QGraphicsItem`.
**Requirement**: CARD-02..03, LINK-01..03, LINK-05, LANE-02..05

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] The scene renders named timeline regions and one visual instance per membership.
- [x] Cards can be moved and emit their updated membership position.
- [x] Directed connections are rendered between valid endpoint instances and remain selectable.
- [x] Shared cards render in each timeline without changing their model identifier.
- [x] Build gate passes: `python -m compileall src`.

**Tests**: none
**Gate**: build
**Commit**: `feat(timeline-editor): add graphics scene editor`

### T5: Implement the main window controller

**What**: Add the main window, menus, file dialogs, card/timeline actions, dirty-state tracking, and model-scene coordination.
**Where**: `src/time_spock/ui/main_window.py`
**Depends on**: T4
**Reuses**: `EditorScene`, `Project`, `ProjectStore`, Qt actions, dialogs, and message boxes.
**Requirement**: CARD-01..06, LINK-01..05, LANE-01..05, FILE-03..05

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [x] The window exposes actions for creating, editing, moving, connecting, and deleting objects.
- [x] Open, Save, Save As, and new-project flows use the storage component.
- [x] Failed loads preserve the active project and unsaved changes prompt before destructive actions.
- [x] Build gate passes: `python -m compileall src`.

**Tests**: none
**Gate**: build
**Commit**: `feat(timeline-editor): add editor window controller`

### T6: Add the application entry point

**What**: Add the package entry point that creates the Qt application and displays the main window.
**Where**: `src/time_spock/main.py`
**Depends on**: T5
**Reuses**: `MainWindow` and PySide6 application lifecycle.
**Requirement**: Enables all P1 stories through the runnable desktop application.

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [ ] `python -m time_spock` starts the desktop application.
- [ ] The application creates exactly one main window and returns the Qt event-loop status.
- [ ] Full gate passes: `python -m pytest; python -m compileall src`.

**Tests**: none
**Gate**: full
**Commit**: `feat(timeline-editor): add desktop application entry point`

### T7: Document and run manual acceptance

**What**: Add the manual acceptance checklist and verify the complete editor workflow against every user story.
**Where**: `docs/manual-acceptance.md`
**Depends on**: T6
**Reuses**: The running application and all prior components.
**Requirement**: CARD-01..06, LINK-01..05, LANE-01..05, FILE-01..05

**Tools**:

- MCP: NONE
- Skill: `tlc-spec-driven`

**Done when**:

- [ ] The checklist covers creation, editing, coloring, moving, branching, deletion, shared cards, multiple timelines, save, open, Save As, and failure prompts.
- [ ] The checklist records a successful run of the complete MVP workflow.
- [ ] Build gate passes: `python -m compileall src; python -m pytest`.

**Tests**: manual
**Gate**: build
**Commit**: `test(timeline-editor): add manual mvp acceptance checklist`

## Phase Execution Map

```text
Phase 1 -> Phase 2 -> Phase 3

Phase 1: T1
Phase 2: T1 -> T2 -> T3
Phase 3: T3 -> T4 -> T5 -> T6 -> T7
```

## Diagram-Definition Cross-Check

| Task | Depends on | Diagram shows | Status |
| --- | --- | --- | --- |
| T1 | None | None | OK |
| T2 | T1 | T1 -> T2 | OK |
| T3 | T2 | T2 -> T3 | OK |
| T4 | T3 | T3 -> T4 | OK |
| T5 | T4 | T4 -> T5 | OK |
| T6 | T5 | T5 -> T6 | OK |
| T7 | T6 | T6 -> T7 | OK |

## Test Co-location Validation

| Task | Code layer | Matrix requires | Task says | Status |
| --- | --- | --- | --- | --- |
| T1 | Configuration | none | none | OK |
| T2 | Domain model | unit | unit | OK |
| T3 | JSON repository | integration | integration | OK |
| T4 | Desktop UI | manual | none | OK: manual acceptance is consolidated in T7 |
| T5 | Desktop UI | manual | none | OK: manual acceptance is consolidated in T7 |
| T6 | Entry point | none | none | OK |
| T7 | Desktop UI | manual | manual | OK |

## Task Granularity Check

| Task | Scope | Status |
| --- | --- | --- |
| T1 | One project configuration file | Granular |
| T2 | One domain component with co-located unit tests | Granular |
| T3 | One persistence component with co-located integration tests | Granular |
| T4 | One graphics scene component | Granular |
| T5 | One window/controller component | Granular |
| T6 | One application entry point | Granular |
| T7 | One manual acceptance artifact | Granular |

**Task validation verdict**: all tasks are atomic, dependencies are backward and diagram-matched, and test fields match the coverage matrix.