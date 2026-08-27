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
- **Phase / Task**: Execute / T7 - manual MVP acceptance
- **Completed**: T1-T6; 14 automated tests passing; compileall passing
- **In-progress**: `docs/manual-acceptance.md` - waiting for visual workflow confirmation
- **Next step**: Run the manual checklist, record its result, then commit T7 and run independent feature validation.
- **Blockers**: User visual acceptance is required for GUI behavior.
- **Uncommitted files**: `.specs/STATE.md`, `.specs/features/timeline-editor/spec.md`, `.specs/features/timeline-editor/context.md`, `.specs/features/timeline-editor/design.md`, `docs/manual-acceptance.md`
- **Branch**: main