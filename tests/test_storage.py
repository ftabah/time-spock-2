import json

import pytest

from time_spock.model import Project
from time_spock.storage import ProjectFileError, ProjectStore


def test_save_and_load_preserves_complete_project(tmp_path):
    project = Project()
    shared = project.add_card("Shared", "Description", "#123456")
    target = project.add_card("Target")
    first = project.add_timeline("Main")
    second = project.add_timeline("Parallel")
    project.add_membership(shared.id, first.id, 10, 20)
    project.add_membership(shared.id, second.id, 300, 400)
    project.add_membership(target.id, second.id, 500, 600)
    connection = project.add_connection(shared.id, target.id)
    path = tmp_path / "story.json"

    ProjectStore.save(project, path)
    loaded = ProjectStore.load(path)

    assert loaded.cards[shared.id].__dict__ == project.cards[shared.id].__dict__
    assert loaded.timelines[first.id].name == "Main"
    assert {(item.card_id, item.timeline_id, item.x, item.y) for item in loaded.memberships} == {
        (shared.id, first.id, 10, 20),
        (shared.id, second.id, 300, 400),
        (target.id, second.id, 500, 600),
    }
    assert loaded.connections[connection.id].source_id == shared.id
    assert loaded.connections[connection.id].target_id == target.id
    assert json.loads(path.read_text(encoding="utf-8"))["schema_version"] == 1


def test_empty_project_can_be_saved_and_loaded(tmp_path):
    path = tmp_path / "empty.json"

    ProjectStore.save(Project(), path)
    loaded = ProjectStore.load(path)

    assert loaded.cards == {}
    assert loaded.timelines == {}
    assert loaded.memberships == []
    assert loaded.connections == {}


def test_missing_or_malformed_file_raises_project_file_error(tmp_path):
    missing = tmp_path / "missing.json"
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not json", encoding="utf-8")

    with pytest.raises(ProjectFileError, match="Unable to read"):
        ProjectStore.load(missing)
    with pytest.raises(ProjectFileError, match="Unable to read"):
        ProjectStore.load(malformed)


def test_incompatible_schema_is_rejected(tmp_path):
    path = tmp_path / "future.json"
    path.write_text(json.dumps({"schema_version": 99}), encoding="utf-8")

    with pytest.raises(ProjectFileError, match="Unsupported"):
        ProjectStore.load(path)


def test_invalid_references_are_rejected_without_returning_partial_project(tmp_path):
    path = tmp_path / "invalid.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "cards": [],
                "timelines": [{"id": "timeline", "name": "Main"}],
                "memberships": [{"card_id": "missing", "timeline_id": "timeline", "x": 0, "y": 0}],
                "connections": [],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ProjectFileError, match="membership references"):
        ProjectStore.load(path)