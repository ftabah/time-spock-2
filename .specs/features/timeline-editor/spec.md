# Timeline Editor Specification

## Problem Statement

Story planning needs a visual way to represent events, branches, and relationships without forcing a single linear structure. The application will let one desktop user create connected cards, arrange them freely, and save the resulting timelines locally.

## Goals

- [ ] Let a user build a story from editable visual cards and directed connections.
- [ ] Let a user display and edit multiple timelines in the same project.
- [ ] Preserve the complete project state in a portable local JSON file.

## Out of Scope

| Feature | Reason |
| --- | --- |
| User accounts and authentication | The MVP is local and single-user. |
| Cloud storage and synchronization | No remote backend is required for the first increment. |
| Automatic chronological validation | Visual position communicates order; the graph has no enforced logical ordering. |
| Collaborative editing | Concurrency between users is outside the MVP. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Desktop technology | Python with PySide6 | Matches the user's language preference and provides native desktop UI capabilities. | yes |
| Timeline meaning | A named visual lane or view in the project | Multiple lanes organize parallel story perspectives without imposing graph semantics. | yes |
| Card ownership | Cards belong to the project and may be placed on multiple timelines | The user explicitly wants one card to appear in both timelines. | yes |
| Connection ownership | Connections reference cards globally and may cross timeline boundaries | A card can branch to events represented in parallel timelines. | yes |
| Visual ordering | Free two-dimensional card position | The user explicitly wants to move cards freely and use position as visual order. | yes |
| File interaction | Local JSON files through Open, Save, and Save As | Keeps the MVP portable and offline. | yes |
| Unsaved changes prompt | The application will ask before discarding unsaved changes | Prevents accidental loss during open, new, or close actions. | no |
| Empty and invalid files | The application will show an actionable error and keep the current project unchanged | A failed load must not destroy the active work. | no |

**Open questions:** none - all unresolved implementation details are recorded as assumptions above.

## User Stories

### P1: Build and Arrange Story Cards * MVP

**User Story**: As a story planner, I want to create and edit colored cards so that I can represent story events visually.

**Why P1**: Cards are the primary content of the application.

**Acceptance Criteria**:

1. WHEN the user creates a card THEN the system SHALL add one card to the active project with a non-empty title, an optional description, a default color, and a unique identifier. <!-- CARD-01 -->
2. WHEN the user edits a card THEN the system SHALL persist the changed title, description, or color in the active project state. <!-- CARD-02 -->
3. WHEN the user moves a card THEN the system SHALL persist its new two-dimensional position in the active project state. <!-- CARD-03 -->
4. IF the user attempts to create or save a card with an empty title THEN the system SHALL reject the operation and keep the previous card state unchanged. <!-- CARD-04 -->
5. WHEN the user deletes a card THEN the system SHALL remove that card and every connection that references its identifier. <!-- CARD-05 -->
6. WHEN the user deletes a card THEN the system SHALL preserve every other card and every connection that does not reference the deleted identifier. <!-- CARD-06 -->

**Independent Test**: Create three cards, edit their content and colors, move them, delete the middle card, and verify that the remaining cards and unrelated connections remain.

### P1: Represent Branching Relationships * MVP

**User Story**: As a story planner, I want directed connections between cards so that I can represent causality, sequence, and parallel events.

**Why P1**: Connections express the relationships that make the visual plan useful for storytelling.

**Acceptance Criteria**:

1. WHEN the user connects a source card to a target card THEN the system SHALL create one directed connection from the source identifier to the target identifier. <!-- LINK-01 -->
2. WHEN a card has multiple incoming or outgoing connections THEN the system SHALL preserve and display every valid connection independently. <!-- LINK-02 -->
3. WHEN the user removes a connection THEN the system SHALL remove only the selected connection and preserve both endpoint cards. <!-- LINK-03 -->
4. IF the user attempts to create a connection whose source or target does not exist THEN the system SHALL reject the operation and preserve the existing project state. <!-- LINK-04 -->
5. The system SHALL allow a connection between cards displayed on different timelines. <!-- LINK-05 -->

**Independent Test**: Create a branching graph with one source, two targets, and a shared target, then remove one connection and verify all other links and cards.

### P1: Work With Multiple Timelines * MVP

**User Story**: As a story planner, I want to create and view multiple timelines together so that I can develop parallel story paths.

**Why P1**: Parallel timelines are central to the user's story model.

**Acceptance Criteria**:

1. WHEN the user creates a timeline THEN the system SHALL add a named timeline to the project and make it available for display. <!-- LANE-01 -->
2. WHEN multiple timelines exist THEN the system SHALL display them simultaneously with distinct names. <!-- LANE-02 -->
3. WHEN the user places a card on a timeline THEN the system SHALL persist that card's membership and visual position for that timeline. <!-- LANE-03 -->
4. WHEN the user places the same card on multiple timelines THEN the system SHALL display that card in each selected timeline without creating duplicate card identities. <!-- LANE-04 -->
5. WHEN the user removes a card from a timeline THEN the system SHALL remove only that timeline membership and preserve the card and its other memberships. <!-- LANE-05 -->

**Independent Test**: Create two named timelines, place one shared card and separate cards on them, then remove the shared card from one timeline and verify it remains in the other.

### P1: Save and Load Projects * MVP

**User Story**: As a story planner, I want to save and reopen my project so that I can continue working later.

**Why P1**: Persistence is required for a practical desktop planning tool.

**Acceptance Criteria**:

1. WHEN the user saves a project THEN the system SHALL write a JSON file containing all cards, titles, descriptions, colors, identifiers, timeline memberships, positions, connections, and timeline names. <!-- FILE-01 -->
2. WHEN the user opens a valid project JSON file THEN the system SHALL reconstruct the saved cards, memberships, positions, connections, and timeline names. <!-- FILE-02 -->
3. IF the selected project file is missing, malformed, or incompatible THEN the system SHALL show an error and leave the current project state unchanged. <!-- FILE-03 -->
4. WHEN the user chooses Save As THEN the system SHALL write the current project to the selected new file path without changing the project contents. <!-- FILE-04 -->
5. IF the project has unsaved changes and the user starts a destructive file action THEN the system SHALL request confirmation before discarding those changes. <!-- FILE-05 -->

**Independent Test**: Build a project with shared cards, branches, custom colors, and moved positions, save it, reopen it, and compare the reconstructed state.

## Edge Cases

- IF a project contains no cards THEN the system SHALL allow it to be saved and reopened as an empty project.
- IF a connection is selected for deletion THEN the system SHALL delete only that connection.
- IF a timeline is empty THEN the system SHALL preserve and display the timeline name.
- IF a file load fails THEN the system SHALL preserve the project that was active before the load attempt.

## Requirement Traceability

| Requirement ID | Story | Phase | Status |
| --- | --- | --- | --- |
| CARD-01 | P1: Build and Arrange Story Cards | Design | Pending |
| CARD-02 | P1: Build and Arrange Story Cards | Design | Pending |
| CARD-03 | P1: Build and Arrange Story Cards | Design | Pending |
| CARD-04 | P1: Build and Arrange Story Cards | Design | Pending |
| CARD-05 | P1: Build and Arrange Story Cards | Design | Pending |
| CARD-06 | P1: Build and Arrange Story Cards | Design | Pending |
| LINK-01 | P1: Represent Branching Relationships | Design | Pending |
| LINK-02 | P1: Represent Branching Relationships | Design | Pending |
| LINK-03 | P1: Represent Branching Relationships | Design | Pending |
| LINK-04 | P1: Represent Branching Relationships | Design | Pending |
| LINK-05 | P1: Represent Branching Relationships | Design | Pending |
| LANE-01 | P1: Work With Multiple Timelines | Design | Pending |
| LANE-02 | P1: Work With Multiple Timelines | Design | Pending |
| LANE-03 | P1: Work With Multiple Timelines | Design | Pending |
| LANE-04 | P1: Work With Multiple Timelines | Design | Pending |
| LANE-05 | P1: Work With Multiple Timelines | Design | Pending |
| FILE-01 | P1: Save and Load Projects | Design | Pending |
| FILE-02 | P1: Save and Load Projects | Design | Pending |
| FILE-03 | P1: Save and Load Projects | Design | Pending |
| FILE-04 | P1: Save and Load Projects | Design | Pending |
| FILE-05 | P1: Save and Load Projects | Design | Pending |

**Coverage:** 22 total, 0 mapped to tasks, 22 pending design.

## Success Criteria

- [ ] A user can create a branching multi-timeline story, save it, close the application, reopen it, and recover the same project state.
- [ ] Deleting one card or connection never deletes unrelated cards or connections.
- [ ] A shared card can appear on two timelines without becoming two independent cards.