from __future__ import annotations

import json
from pathlib import Path

from time_spock.model import Card, Connection, Membership, Project, Timeline


SCHEMA_VERSION = 1


class ProjectFileError(ValueError):
    pass


class ProjectStore:
    @staticmethod
    def save(project: Project, path: str | Path) -> None:
        payload = {
            "schema_version": SCHEMA_VERSION,
            "cards": [card.__dict__ for card in project.cards.values()],
            "timelines": [timeline.__dict__ for timeline in project.timelines.values()],
            "memberships": [membership.__dict__ for membership in project.memberships],
            "connections": [connection.__dict__ for connection in project.connections.values()],
        }
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @staticmethod
    def load(path: str | Path) -> Project:
        try:
            payload = json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ProjectFileError(f"Unable to read project file: {path}") from error

        if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
            raise ProjectFileError("Unsupported project file schema")
        if any(not isinstance(payload.get(key), list) for key in ("cards", "timelines", "memberships", "connections")):
            raise ProjectFileError("Project file collections are invalid")

        try:
            project = Project(
                cards={item["id"]: Card(**item) for item in payload["cards"]},
                timelines={item["id"]: Timeline(**item) for item in payload["timelines"]},
                memberships=[Membership(**item) for item in payload["memberships"]],
                connections={item["id"]: Connection(**item) for item in payload["connections"]},
            )
        except (KeyError, TypeError) as error:
            raise ProjectFileError("Project file contains invalid records") from error

        if any(
            membership.card_id not in project.cards or membership.timeline_id not in project.timelines
            for membership in project.memberships
        ):
            raise ProjectFileError("Project file contains invalid membership references")
        if any(
            connection.source_id not in project.cards or connection.target_id not in project.cards
            for connection in project.connections.values()
        ):
            raise ProjectFileError("Project file contains invalid connection references")
        return project