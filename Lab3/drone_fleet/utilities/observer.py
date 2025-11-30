from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any


class Observer(ABC):
    """Observer interface for reacting to FleetManager events."""

    @abstractmethod
    def update(self, event: str, payload: Dict[str, Any]) -> None:
        pass


class ConsoleObserver(Observer):
    """Simple concrete observer printing events (demo purpose)."""

    def update(self, event: str, payload: Dict[str, Any]) -> None:  # noqa: D401
        print(f"[OBS] {event} -> {payload}")


class MissionCountObserver(Observer):
    """Tracks number of missions created/adapted/assigned."""

    def __init__(self) -> None:
        self.created = 0
        self.assigned = 0

    def update(self, event: str, payload: Dict[str, Any]) -> None:
        if event in {"mission.adapted"}:
            self.created += 1
        if event == "mission.assigned":
            self.assigned += 1

    def stats(self) -> str:
        return f"missions_created={self.created}, missions_assigned={self.assigned}"