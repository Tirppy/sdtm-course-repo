from typing import List, Optional
from drone_fleet.models.mission import Mission


class MissionBuilder:
    """Fluent builder for Mission objects."""

    def __init__(self) -> None:
        self._name: Optional[str] = None
        self._waypoints: List[str] = []
        self._duration: Optional[int] = None
        self._priority: int = 3
        self._payload: Optional[str] = None

    def name(self, name: str) -> 'MissionBuilder':
        self._name = name
        return self

    def add_waypoint(self, waypoint: str) -> 'MissionBuilder':
        self._waypoints.append(waypoint)
        return self

    def duration(self, minutes: int) -> 'MissionBuilder':
        self._duration = minutes
        return self

    def priority(self, priority: int) -> 'MissionBuilder':
        self._priority = priority
        return self

    def payload(self, payload: str) -> 'MissionBuilder':
        self._payload = payload
        return self

    def build(self) -> Mission:
        if self._name is None:
            raise ValueError("Mission name not set")
        if self._duration is None:
            raise ValueError("Mission duration not set")
        return Mission(
            name=self._name,
            waypoints=self._waypoints,
            duration_minutes=self._duration,
            priority=self._priority,
            payload=self._payload
        )
