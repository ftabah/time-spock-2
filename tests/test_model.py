import pytest

from time_spock.model import Project


def test_add_card_creates_unique_card_with_default_and_optional_values():
    project = Project()

    first = project.add_card("Opening", "The story starts", "#123456")
    second = project.add_card("Ending")

    assert first.id != second.id
    assert project.cards[first.id].title == "Opening"
    assert project.cards[first.id].description == "The story starts"
    assert project.cards[first.id].color == "#123456"
    assert project.cards[second.id].description == ""
    assert project.cards[second.id].color == "#f4c95d"


def test_card_updates_preserve_and_change_requested_fields():
    project = Project()
    card = project.add_card("Draft", "Old description", "#111111")

    project.update_card(card.id, title="Final", description="New description", color="#222222")

    assert project.cards[card.id].title == "Final"
    assert project.cards[card.id].description == "New description"
    assert project.cards[card.id].color == "#222222"


def test_empty_card_title_is_rejected_without_changing_project():
    project = Project()
    card = project.add_card("Existing", "Description", "#111111")

    with pytest.raises(ValueError, match="Card title"):
        project.add_card("   ")
    with pytest.raises(ValueError, match="Card title"):
        project.update_card(card.id, title="")

    assert list(project.cards) == [card.id]
    assert project.cards[card.id].title == "Existing"


def test_membership_position_is_independent_per_timeline():
    project = Project()
    card = project.add_card("Shared event")
    first_timeline = project.add_timeline("Main")
    second_timeline = project.add_timeline("Parallel")

    first_membership = project.add_membership(card.id, first_timeline.id, 10, 20)
    second_membership = project.add_membership(card.id, second_timeline.id, 300, 400)
    project.update_membership_position(card.id, first_timeline.id, 50, 60)

    assert first_membership.x == 50
    assert first_membership.y == 60
    assert second_membership.x == 300
    assert second_membership.y == 400
    assert len(project.cards) == 1


def test_next_card_position_does_not_fully_overlap_existing_cards():
    project = Project()
    timeline = project.add_timeline("Main")
    first = project.add_card("First")
    second = project.add_card("Second")
    project.add_membership(first.id, timeline.id, 40, 60)

    x, y = project.next_card_position(timeline.id)
    project.add_membership(second.id, timeline.id, x, y)

    assert (x, y) != (40, 60)
    assert project.memberships[1].card_id == second.id


def test_connections_preserve_direction_and_allow_branching():
    project = Project()
    source = project.add_card("Source")
    target_a = project.add_card("Target A")
    target_b = project.add_card("Target B")

    first = project.add_connection(source.id, target_a.id)
    second = project.add_connection(source.id, target_b.id)
    third = project.add_connection(target_a.id, target_b.id)

    assert project.connections[first.id].source_id == source.id
    assert project.connections[first.id].target_id == target_a.id
    assert len(project.connections) == 3
    assert project.connections[second.id].source_id == source.id
    assert project.connections[third.id].target_id == target_b.id


def test_invalid_connection_reference_is_rejected_without_state_change():
    project = Project()
    source = project.add_card("Source")

    with pytest.raises(ValueError, match="Card"):
        project.add_connection(source.id, "missing")

    assert project.connections == {}


def test_deleting_card_removes_only_related_memberships_and_connections():
    project = Project()
    deleted = project.add_card("Deleted")
    preserved = project.add_card("Preserved")
    other = project.add_card("Other")
    timeline = project.add_timeline("Main")
    project.add_membership(deleted.id, timeline.id, 0, 0)
    project.add_membership(preserved.id, timeline.id, 100, 100)
    related = project.add_connection(deleted.id, preserved.id)
    unrelated = project.add_connection(preserved.id, other.id)

    project.delete_card(deleted.id)

    assert deleted.id not in project.cards
    assert preserved.id in project.cards
    assert other.id in project.cards
    assert all(membership.card_id != deleted.id for membership in project.memberships)
    assert related.id not in project.connections
    assert unrelated.id in project.connections


def test_removing_one_connection_preserves_endpoint_cards_and_other_connections():
    project = Project()
    source = project.add_card("Source")
    first_target = project.add_card("First")
    second_target = project.add_card("Second")
    removed = project.add_connection(source.id, first_target.id)
    preserved = project.add_connection(source.id, second_target.id)

    project.remove_connection(removed.id)

    assert removed.id not in project.connections
    assert preserved.id in project.connections
    assert source.id in project.cards
    assert first_target.id in project.cards
    assert second_target.id in project.cards


def test_membership_requires_existing_card_and_timeline():
    project = Project()
    timeline = project.add_timeline("Main")

    with pytest.raises(ValueError, match="Card"):
        project.add_membership("missing", timeline.id, 0, 0)
    with pytest.raises(ValueError, match="Timeline"):
        project.add_membership(project.add_card("Event").id, "missing", 0, 0)

    assert project.memberships == []