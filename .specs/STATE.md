# STATE

## Decisions

### AD-001
- **Decision**: The application will use Python with PySide6 and `QGraphicsScene` for its desktop visual editor.
- **Reason**: This matches the user's language preference and provides the interaction primitives needed for movable cards and graph connections.
- **Trade-off**: The project adds the PySide6 dependency and does not use a zero-dependency standard-library GUI.
- **Scope**: All desktop UI features in this project.
- **Date**: 2026-08-27
- **Status**: active

## Handoff

- **Feature**: timeline-editor
- **Phase / Task**: Design complete
- **Completed**: specification, context, architecture design
- **In-progress**: none
- **Next step**: Confirm the design, then break the implementation into atomic tasks.
- **Blockers**: none
- **Uncommitted files**: `.specs/STATE.md`, `.specs/features/timeline-editor/spec.md`, `.specs/features/timeline-editor/context.md`, `.specs/features/timeline-editor/design.md`
- **Branch**: main