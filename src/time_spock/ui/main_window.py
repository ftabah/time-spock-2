from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QFileDialog,
    QGraphicsView,
    QInputDialog,
    QMainWindow,
    QMessageBox,
)

from time_spock.model import Project
from time_spock.storage import ProjectFileError, ProjectStore
from time_spock.ui.scene import CardItem, ConnectionItem, EditorScene


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.project = Project()
        self.store = ProjectStore()
        self.file_path: Path | None = None
        self.dirty = False
        self.scene = EditorScene(self)
        self.scene.card_moved.connect(self._on_card_moved)
        self.scene.connection_requested.connect(self._on_connection_requested)
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Time Spock")
        self.resize(1100, 700)
        self._create_actions()
        self._render()

    def _create_actions(self) -> None:
        file_menu = self.menuBar().addMenu("File")
        edit_menu = self.menuBar().addMenu("Edit")
        timeline_menu = self.menuBar().addMenu("Timeline")

        self._add_action(file_menu, "New", self.new_project)
        self._add_action(file_menu, "Open", self.open_project)
        self._add_action(file_menu, "Save", self.save_project)
        self._add_action(file_menu, "Save As", self.save_project_as)
        self._add_action(edit_menu, "Add Card", self.add_card)
        self._add_action(edit_menu, "Edit Card", self.edit_card)
        self._add_action(edit_menu, "Delete Card", self.delete_card)
        self._add_action(edit_menu, "Remove Card From Timeline", self.remove_card_from_timeline)
        self._add_action(edit_menu, "Connect Selected Cards", self.connect_selected_cards)
        self._add_action(edit_menu, "Delete Selected Connection", self.delete_selected_connection)
        self._add_action(timeline_menu, "Add Timeline", self.add_timeline)

    @staticmethod
    def _add_action(menu, label: str, handler) -> QAction:
        action = QAction(label, menu)
        action.triggered.connect(handler)
        menu.addAction(action)
        return action

    def _render(self) -> None:
        self.scene.render(self.project)

    def _on_card_moved(self, card_id: str, timeline_id: str, x: float, y: float) -> None:
        self.project.update_membership_position(card_id, timeline_id, x, y - 28)
        self._mark_dirty()

    def _on_connection_requested(self, source_id: str, target_id: str) -> None:
        try:
            self.project.add_connection(source_id, target_id)
        except ValueError:
            return
        self._mark_dirty()
        self._render()

    def _mark_dirty(self) -> None:
        self.dirty = True
        self._update_title()

    def _update_title(self) -> None:
        name = self.file_path.name if self.file_path else "Untitled"
        self.setWindowTitle(f"Time Spock - {name}{' *' if self.dirty else ''}")

    def new_project(self) -> None:
        if not self.confirm_discard_if_dirty():
            return
        self.project = Project()
        self.file_path = None
        self.dirty = False
        self._render()
        self._update_title()

    def open_project(self) -> None:
        if not self.confirm_discard_if_dirty():
            return
        path, _ = QFileDialog.getOpenFileName(self, "Open Project", "", "Time Spock (*.json)")
        if not path:
            return
        try:
            project = self.store.load(path)
        except ProjectFileError as error:
            QMessageBox.critical(self, "Unable to open project", str(error))
            return
        self.project = project
        self.file_path = Path(path)
        self.dirty = False
        self._render()
        self._update_title()

    def save_project(self) -> None:
        if self.file_path is None:
            self.save_project_as()
            return
        self._save_to(self.file_path)

    def save_project_as(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Time Spock (*.json)")
        if path:
            self.file_path = Path(path)
            self._save_to(self.file_path)

    def _save_to(self, path: Path) -> None:
        try:
            self.store.save(self.project, path)
        except OSError as error:
            QMessageBox.critical(self, "Unable to save project", str(error))
            return
        self.dirty = False
        self._update_title()

    def confirm_discard_if_dirty(self) -> bool:
        if not self.dirty:
            return True
        choice = QMessageBox.question(
            self,
            "Unsaved changes",
            "Save changes before continuing?",
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel,
        )
        if choice == QMessageBox.StandardButton.Save:
            self.save_project()
            return not self.dirty
        return choice == QMessageBox.StandardButton.Discard

    def add_card(self) -> None:
        title, accepted = QInputDialog.getText(self, "Add Card", "Title:")
        if not accepted or not title.strip():
            return
        description, accepted = QInputDialog.getMultiLineText(self, "Add Card", "Description:")
        if not accepted:
            return
        color = QColorDialog.getColor(QColor("#f4c95d"), self, "Card Color")
        if not color.isValid():
            return
        card = self.project.add_card(title, description, color.name())
        timeline = next(iter(self.project.timelines.values()), None)
        if timeline is None:
            timeline = self.project.add_timeline("Main")
        x, y = self.project.next_card_position(timeline.id)
        self.project.add_membership(card.id, timeline.id, x, y)
        self._mark_dirty()
        self._render()

    def edit_card(self) -> None:
        item = self._selected_card()
        if item is None:
            return
        card = self.project.cards[item.card_id]
        title, accepted = QInputDialog.getText(self, "Edit Card", "Title:", text=card.title)
        if not accepted or not title.strip():
            return
        description, accepted = QInputDialog.getMultiLineText(
            self, "Edit Card", "Description:", text=card.description
        )
        if not accepted:
            return
        color = QColorDialog.getColor(QColor(card.color), self, "Card Color")
        if not color.isValid():
            return
        self.project.update_card(item.card_id, title=title, description=description, color=color.name())
        self._mark_dirty()
        self._render()

    def add_timeline(self) -> None:
        name, accepted = QInputDialog.getText(self, "Add Timeline", "Name:")
        if accepted and name.strip():
            self.project.add_timeline(name)
            self._mark_dirty()
            self._render()

    def delete_card(self) -> None:
        item = self._selected_card()
        if item is not None:
            self.project.delete_card(item.card_id)
            self._mark_dirty()
            self._render()

    def remove_card_from_timeline(self) -> None:
        item = self._selected_card()
        if item is not None:
            self.project.remove_membership(item.card_id, item.timeline_id)
            self._mark_dirty()
            self._render()

    def connect_selected_cards(self) -> None:
        cards = [item for item in self.scene.selectedItems() if isinstance(item, CardItem)]
        if len(cards) == 2:
            self.project.add_connection(cards[0].card_id, cards[1].card_id)
            self._mark_dirty()
            self._render()

    def delete_selected_connection(self) -> None:
        connections = [item for item in self.scene.selectedItems() if isinstance(item, ConnectionItem)]
        if connections:
            self.project.remove_connection(connections[0].connection_id)
            self._mark_dirty()
            self._render()

    def _selected_card(self) -> CardItem | None:
        return next((item for item in self.scene.selectedItems() if isinstance(item, CardItem)), None)

    def closeEvent(self, event) -> None:
        if self.confirm_discard_if_dirty():
            event.accept()
        else:
            event.ignore()