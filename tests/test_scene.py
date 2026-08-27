import pytest

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtWidgets import QApplication

from time_spock.model import Project
from time_spock.ui.scene import EditorScene


@pytest.fixture(scope="session")
def qt_app():
    return QApplication.instance() or QApplication([])


def test_connection_path_ends_on_card_borders_and_tracks_movement(qt_app):
    project = Project()
    source = project.add_card("Source")
    target = project.add_card("Target")
    timeline = project.add_timeline("Main")
    project.add_membership(source.id, timeline.id, 40, 60)
    project.add_membership(target.id, timeline.id, 300, 60)
    connection = project.add_connection(source.id, target.id)
    scene = EditorScene()
    scene.render(project)

    line = scene.connection_items[connection.id]
    start = line.path().elementAt(0)
    end = line.path().elementAt(1)
    source_rect = QRectF(40, 88, 180, 100)
    target_rect = QRectF(300, 88, 180, 100)
    assert start.x == source_rect.right()
    assert end.x == target_rect.left()

    scene.card_items[(target.id, timeline.id)].setPos(QPointF(400, 180))

    moved_end = line.path().elementAt(1)
    assert moved_end.x == 400
    assert moved_end.y == 207