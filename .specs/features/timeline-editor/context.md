# Timeline Editor Context

**Gathered:** 2026-08-27
**Spec:** `.specs/features/timeline-editor/spec.md`
**Status:** Ready for design

## Feature Boundary

The MVP is a local desktop editor for cards, directed connections, multiple simultaneous timelines, and JSON project files. It is a single-user application with free visual positioning and no enforced logical chronology.

## Implementation Decisions

### Platform and language

- Use Python with PySide6 for the desktop application.
- Use local JSON files for project persistence.
- Do not add accounts, cloud storage, synchronization, or collaboration.

### Story graph

- Connections are directional.
- A card may have multiple incoming and outgoing connections.
- Connections may cross timeline boundaries.
- Cards are globally identified within the project.

### Timelines and positioning

- Multiple timelines are visible at the same time.
- A card may appear on more than one timeline without duplication.
- Timelines organize visual perspectives or parallel paths.
- Card positions are freely editable in two dimensions.
- Position communicates visual order; the application does not enforce chronology or validate ordering.
- New cards must be placed without fully overlapping an existing card in their initial timeline.
- Card size is editable per timeline membership and is saved with that membership.

### Visual editing

- Connections are displayed as visible lines with arrowheads.
- Connection creation remains available through the existing card-selection/menu flow.
- A card has a visible resize handle at its lower-right border.
- Dragging the left mouse button on empty canvas space pans the view.
- Right-clicking a connection offers an action to invert its direction.
- Connections have a larger invisible hit area than their visible stroke.
- Right-clicking a connection also offers an action to remove it.
- Holding `Ctrl` while using the mouse wheel zooms the canvas around the cursor.

### Agent's Discretion

- Exact canvas interaction details, file schema versioning, default card placement, and visual styling remain implementation decisions during design.
- The application will use standard desktop confirmation and error dialogs unless later discussion changes that choice.

### Declined / Undiscussed Gray Areas -> Assumptions

- Unsaved-change confirmation and invalid-file behavior are recorded as defaults in the specification because they protect user work and do not expand MVP scope.

## Specific References

The user described parallel events where one event can point to multiple events and be pointed to by multiple events. The same card may appear in two timelines simultaneously.

## Deferred Ideas

None - discussion stayed within MVP scope.