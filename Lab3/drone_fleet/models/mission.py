from typing import List, Optional


class Mission:
    """Value object holding mission data."""

    def __init__(self, name: str, waypoints: List[str], duration_minutes: int,
                 priority: int = 3, payload: Optional[str] = None) -> None:
        if not name:
            raise ValueError("Mission name is required")
        if duration_minutes <= 0:
            raise ValueError("Mission duration must be positive")
        if not waypoints:
            raise ValueError("Mission requires at least one waypoint")
        self._name = name
        self._waypoints = list(waypoints)
        self._duration_minutes = duration_minutes
        self._priority = priority
        self._payload = payload

    @property
    def name(self) -> str:
        return self._name

    @property
    def waypoints(self) -> List[str]:
        return list(self._waypoints)

    @property
    def duration_minutes(self) -> int:
        return self._duration_minutes

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def payload(self) -> Optional[str]:
        return self._payload

    def __repr__(self) -> str:
        return (
            f"Mission(name={self._name!r}, waypoints={self._waypoints!r}, "
            f"duration_minutes={self._duration_minutes}, priority={self._priority}, "
            f"payload={self._payload!r})"
        )
