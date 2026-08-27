from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication

from time_spock.ui.main_window import CanvasView


def test_zoom_at_changes_scale_within_navigation_limits():
    app = QApplication.instance() or QApplication([])
    view = CanvasView(None)

    view.zoom_at(1.15, QPoint(100, 100))
    assert view.zoom_level == 1.15
    assert view.transform().m11() == 1.15

    view.zoom_at(1 / 1.15, QPoint(100, 100))
    assert round(view.zoom_level, 8) == 1.0
    assert round(view.transform().m11(), 8) == 1.0

    view.zoom_at(0.01, QPoint(100, 100))
    assert view.zoom_level == 0.35
    view.zoom_at(100, QPoint(100, 100))
    assert view.zoom_level == 2.5