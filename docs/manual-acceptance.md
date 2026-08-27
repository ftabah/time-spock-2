# Manual Acceptance: Timeline Editor MVP

Run from the repository root with:

```powershell
$env:PYTHONPATH = "src"
python -m time_spock
```

## Checklist

- [ ] The application opens with a visible editor window.
- [ ] Add a timeline named `Main` and a second timeline named `Parallel`.
- [ ] Add a card with a title, description, and custom color.
- [ ] Add another card and move both cards to different positions.
- [ ] Select two cards and create a directed connection.
- [ ] Verify connecting cards does not change either card's position.
- [ ] Verify the connection line is visible and has an arrowhead at the target card.
- [ ] Move either connected card and verify the line follows it while staying attached to both borders.
- [ ] Drag the left mouse button on empty white canvas space and verify the canvas pans without moving cards.
- [ ] Right-click a connection and choose `Inverter direção da seta`; verify the arrow points to the other card.
- [ ] Right-click near, but not directly on, a connection and verify the connection menu opens.
- [ ] Choose `Remover conexão` and verify only the line disappears while both cards remain.
- [ ] Create a branch from one card to two target cards.
- [ ] Drag the lower-right resize handle of a card and verify its size changes while its position remains fixed.
- [ ] Resize a shared card in one timeline and verify the other timeline keeps its own size.
- [ ] Place one card in both timelines and verify it remains one shared card in the saved data.
- [ ] Remove one card from one timeline and verify its other membership remains.
- [ ] Delete one connection and verify both cards remain.
- [ ] Delete one card and verify its related connections disappear while unrelated cards and connections remain.
- [ ] Save the project as a JSON file.
- [ ] Open the saved JSON file and verify cards, colors, descriptions, positions, timelines, memberships, and connections return.
- [ ] Make a change, choose a destructive file action, and verify the unsaved-changes prompt appears.
- [ ] Attempt to open a malformed JSON file and verify the active project remains unchanged.

## Result

- **Date**: pending
- **Python**: pending
- **Result**: pending
- **Notes**: pending