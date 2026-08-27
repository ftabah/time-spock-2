from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject, QGraphicsPathItem, QGraphicsScene

from time_spock.model import Card, Connection, Membership, Project, Timeline


CARD_WIDTH = 180.0
CARD_HEIGHT = 100.0
TIMELINE_HEIGHT = 180.0


class CardItem(QGraphicsObject):
    moved = Signal(str, str, float, float)
    connection_requested = Signal(str, str)

    def __init__(self, card: Card, membership: Membership, parent: QGraphicsItem | None = None) -> None:
        super().__init__(parent)
        self.card_id = card.id
        self.timeline_id = membership.timeline_id
        self.card = card
        self.connection_dragging = False
        self.setPos(membership.x, membership.y)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
        )

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, CARD_WIDTH, CARD_HEIGHT)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setBrush(QBrush(QColor(self.card.color)))
        painter.setPen(QPen(QColor("#24313a"), 2 if self.isSelected() else 1))
        painter.drawRoundedRect(self.boundingRect(), 8, 8)
        painter.setPen(QPen(QColor("#172026")))
        painter.drawText(QRectF(12, 12, CARD_WIDTH - 24, 28), Qt.AlignmentFlag.AlignLeft, self.card.title)
        painter.drawText(
            QRectF(12, 42, CARD_WIDTH - 24, CARD_HEIGHT - 54),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
            self.card.description,
        )
        painter.setBrush(QBrush(QColor("#24313a")))
        painter.drawEllipse(QRectF(CARD_WIDTH - 14, CARD_HEIGHT / 2 - 6, 12, 12))

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            position = value
            self.moved.emit(self.card_id, self.timeline_id, position.x(), position.y())
        return super().itemChange(change, value)

    def mousePressEvent(self, event) -> None:
        if QRectF(CARD_WIDTH - 24, CARD_HEIGHT / 2 - 16, 24, 32).contains(event.pos()):
            self.connection_dragging = True
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.connection_dragging:
            self.connection_dragging = False
            target = self.scene().itemAt(event.scenePos(), self.scene().views()[0].transform())
            if isinstance(target, CardItem) and target.card_id != self.card_id:
                self.connection_requested.emit(self.card_id, target.card_id)
            event.accept()
            return
        super().mouseReleaseEvent(event)


class ConnectionItem(QGraphicsPathItem):
    def __init__(self, connection: Connection, source: CardItem, target: CardItem) -> None:
        super().__init__()
        self.connection_id = connection.id
        self.source = source
        self.target = target
        self.setZValue(1)
        self.setPen(QPen(QColor("#52616b"), 2))
        self.update_path()

    def update_path(self) -> None:
        start = self.source.pos() + self.source.boundingRect().center()
        end = self.target.pos() + self.target.boundingRect().center()
        path = QPainterPath(start)
        path.lineTo(end)
        self.setPath(path)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        super().paint(painter, option, widget)
        start = self.source.pos() + self.source.boundingRect().center()
        end = self.target.pos() + self.target.boundingRect().center()
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 10
        points = QPolygonF(
            [
                end,
                end - QPointF(arrow_size * math.cos(angle - math.pi / 6), arrow_size * math.sin(angle - math.pi / 6)),
                end - QPointF(arrow_size * math.cos(angle + math.pi / 6), arrow_size * math.sin(angle + math.pi / 6)),
            ]
        )
        painter.setBrush(QBrush(QColor("#52616b")))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(points)


class EditorScene(QGraphicsScene):
    card_moved = Signal(str, str, float, float)
    connection_requested = Signal(str, str)
    delete_selected = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.card_items: dict[tuple[str, str], CardItem] = {}
        self.connection_items: dict[str, ConnectionItem] = {}

    def render(self, project: Project) -> None:
        self.project = project
        self.clear()
        self.card_items.clear()
        self.connection_items.clear()
        for index, timeline in enumerate(project.timelines.values()):
            self._render_timeline(timeline, index)
        for connection in project.connections.values():
            source = self._first_card_item(connection.source_id)
            target = self._first_card_item(connection.target_id)
            if source and target:
                item = ConnectionItem(connection, source, target)
                self.addItem(item)
                self.connection_items[connection.id] = item

    def _render_timeline(self, timeline: Timeline, index: int) -> None:
        y_offset = index * TIMELINE_HEIGHT
        self.addText(timeline.name).setPos(8, y_offset + 8)
        self.addRect(0, y_offset, 1600, TIMELINE_HEIGHT, QPen(QColor("#b7c4c9")))
        for membership in self._memberships_for(timeline.id):
            card = self.project.cards[membership.card_id]
            adjusted = Membership(card.id, timeline.id, membership.x, membership.y + y_offset + 28)
            item = CardItem(card, adjusted)
            item.moved.connect(self.card_moved)
            item.moved.connect(self._refresh_connections)
            item.connection_requested.connect(self.connection_requested)
            self.addItem(item)
            self.card_items[(card.id, timeline.id)] = item

    def _refresh_connections(self, *_args) -> None:
        for item in self.connection_items.values():
            item.update_path()

    def _memberships_for(self, timeline_id: str) -> list[Membership]:
        return [membership for membership in self.project.memberships if membership.timeline_id == timeline_id]

    def _first_card_item(self, card_id: str) -> CardItem | None:
        return next((item for (item_card_id, _), item in self.card_items.items() if item_card_id == card_id), None)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.delete_selected.emit()
        super().keyPressEvent(event)