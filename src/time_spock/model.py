from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Card:
    id: str
    title: str
    description: str
    color: str


@dataclass
class Timeline:
    id: str
    name: str


@dataclass
class Membership:
    card_id: str
    timeline_id: str
    x: float
    y: float
    width: float = 180
    height: float = 100


@dataclass
class Connection:
    id: str
    source_id: str
    target_id: str


@dataclass
class Project:
    cards: dict[str, Card] = field(default_factory=dict)
    timelines: dict[str, Timeline] = field(default_factory=dict)
    memberships: list[Membership] = field(default_factory=list)
    connections: dict[str, Connection] = field(default_factory=dict)

    def add_card(self, title: str, description: str = "", color: str = "#f4c95d") -> Card:
        if not title.strip():
            raise ValueError("Card title cannot be empty")
        card = Card(str(uuid4()), title, description, color)
        self.cards[card.id] = card
        return card

    def update_card(
        self,
        card_id: str,
        *,
        title: str | None = None,
        description: str | None = None,
        color: str | None = None,
    ) -> None:
        card = self._require_card(card_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Card title cannot be empty")
            card.title = title
        if description is not None:
            card.description = description
        if color is not None:
            card.color = color

    def delete_card(self, card_id: str) -> None:
        self._require_card(card_id)
        del self.cards[card_id]
        self.memberships = [membership for membership in self.memberships if membership.card_id != card_id]
        self.connections = {
            connection_id: connection
            for connection_id, connection in self.connections.items()
            if connection.source_id != card_id and connection.target_id != card_id
        }

    def add_timeline(self, name: str) -> Timeline:
        if not name.strip():
            raise ValueError("Timeline name cannot be empty")
        timeline = Timeline(str(uuid4()), name)
        self.timelines[timeline.id] = timeline
        return timeline

    def add_membership(
        self,
        card_id: str,
        timeline_id: str,
        x: float,
        y: float,
        width: float = 180,
        height: float = 100,
    ) -> Membership:
        self._require_card(card_id)
        self._require_timeline(timeline_id)
        membership = Membership(card_id, timeline_id, x, y, max(100, width), max(70, height))
        self.memberships.append(membership)
        return membership

    def next_card_position(self, timeline_id: str, width: float = 180, height: float = 100) -> tuple[float, float]:
        self._require_timeline(timeline_id)
        existing = [membership for membership in self.memberships if membership.timeline_id == timeline_id]
        for row in range(20):
            for column in range(8):
                candidate_x = 40 + column * (width + 20)
                candidate_y = 60 + row * (height + 20)
                if all(
                    candidate_x + width <= membership.x
                    or membership.x + width <= candidate_x
                    or candidate_y + height <= membership.y
                    or membership.y + height <= candidate_y
                    for membership in existing
                ):
                    return candidate_x, candidate_y
        return 40, 60 + len(existing) * (height + 20)

    def remove_membership(self, card_id: str, timeline_id: str) -> None:
        self.memberships = [
            membership
            for membership in self.memberships
            if membership.card_id != card_id or membership.timeline_id != timeline_id
        ]

    def update_membership_position(self, card_id: str, timeline_id: str, x: float, y: float) -> None:
        for membership in self.memberships:
            if membership.card_id == card_id and membership.timeline_id == timeline_id:
                membership.x = x
                membership.y = y
                return
        raise ValueError("Membership does not exist")

    def update_membership_size(self, card_id: str, timeline_id: str, width: float, height: float) -> None:
        for membership in self.memberships:
            if membership.card_id == card_id and membership.timeline_id == timeline_id:
                membership.width = max(100, width)
                membership.height = max(70, height)
                return
        raise ValueError("Membership does not exist")

    def add_connection(self, source_id: str, target_id: str) -> Connection:
        self._require_card(source_id)
        self._require_card(target_id)
        connection = Connection(str(uuid4()), source_id, target_id)
        self.connections[connection.id] = connection
        return connection

    def remove_connection(self, connection_id: str) -> None:
        if connection_id not in self.connections:
            raise ValueError("Connection does not exist")
        del self.connections[connection_id]

    def reverse_connection(self, connection_id: str) -> None:
        connection = self.connections.get(connection_id)
        if connection is None:
            raise ValueError("Connection does not exist")
        connection.source_id, connection.target_id = connection.target_id, connection.source_id

    def _require_card(self, card_id: str) -> Card:
        if card_id not in self.cards:
            raise ValueError("Card does not exist")
        return self.cards[card_id]

    def _require_timeline(self, timeline_id: str) -> Timeline:
        if timeline_id not in self.timelines:
            raise ValueError("Timeline does not exist")
        return self.timelines[timeline_id]