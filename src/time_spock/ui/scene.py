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
    resized = Signal(str, str, float, float)

    def __init__(
        self,
        card: Card,
        membership: Membership,
        timeline_offset: float = 0,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(parent)
        self.card_id = card.id
        self.timeline_id = membership.timeline_id
        self.card = card
        self.resize_dragging = False
        self.width = membership.width
        self.height = membership.height
        self.timeline_offset = timeline_offset
        self.setPos(membership.x, membership.y + timeline_offset)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setBrush(QBrush(QColor(self.card.color)))
        painter.setPen(QPen(QColor("#24313a"), 2 if self.isSelected() else 1))
        painter.drawRoundedRect(self.boundingRect(), 8, 8)
        painter.setPen(QPen(QColor("#172026")))
        painter.drawText(QRectF(12, 12, self.width - 24, 28), Qt.AlignmentFlag.AlignLeft, self.card.title)
        painter.drawText(
            QRectF(12, 42, self.width - 24, self.height - 54),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
            self.card.description,
        )
        painter.setBrush(QBrush(QColor("#52616b")))
        painter.drawRect(QRectF(self.width - 10, self.height - 10, 8, 8))

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            position = value
            self.moved.emit(self.card_id, self.timeline_id, position.x(), position.y() - self.timeline_offset)
        return super().itemChange(change, value)

    def mousePressEvent(self, event) -> None:
        if QRectF(self.width - 20, self.height - 20, 20, 20).contains(event.pos()):
            self.resize_dragging = True
            self.resize_origin = event.scenePos()
            self.resize_size = (self.width, self.height)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.resize_dragging:
            delta = event.scenePos() - self.resize_origin
            self.prepareGeometryChange()
            self.width = max(100, self.resize_size[0] + delta.x())
            self.height = max(70, self.resize_size[1] + delta.y())
            self.resized.emit(self.card_id, self.timeline_id, self.width, self.height)
            self.update()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if self.resize_dragging:
            self.resize_dragging = False
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
        start_center = self.source.sceneBoundingRect().center()
        end_center = self.target.sceneBoundingRect().center()
        start = self._border_point(self.source.sceneBoundingRect(), end_center)
        end = self._border_point(self.target.sceneBoundingRect(), start_center)
        path = QPainterPath(start)
        path.lineTo(end)
        self.setPath(path)

    @staticmethod
    def _border_point(rect: QRectF, toward: QPointF) -> QPointF:
        center = rect.center()
        direction = toward - center
        if direction.isNull():
            return center
        scale_x = rect.width() / (2 * abs(direction.x())) if direction.x() else float("inf")
        scale_y = rect.height() / (2 * abs(direction.y())) if direction.y() else float("inf")
        scale = min(scale_x, scale_y)
        return center + direction * scale

    def paint(self, painter: QPainter, option, widget=None) -> None:
        super().paint(painter, option, widget)
        start_center = self.source.sceneBoundingRect().center()
        end_center = self.target.sceneBoundingRect().center()
        start = self._border_point(self.source.sceneBoundingRect(), end_center)
        end = self._border_point(self.target.sceneBoundingRect(), start_center)
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
    card_resized = Signal(str, str, float, float)
    delete_selected = Signal()
    context_requested = Signal(str, QPointF)

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
            item = CardItem(card, membership, y_offset + 28)
            item.moved.connect(self.card_moved)
            item.moved.connect(self._refresh_connections)
            item.resized.connect(self.card_resized)
            item.resized.connect(self._refresh_connections)
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

    def contextMenuEvent(self, event) -> None:
        item = self.itemAt(event.scenePos(), self.views()[0].transform()) if self.views() else None
        card_id = item.card_id if isinstance(item, CardItem) else ""
        self.context_requested.emit(card_id, event.scenePos())
        event.accept()