from drone_fleet.models.drone import Drone
from typing import Callable, Optional


class DroneProxy(Drone):
    """Lazy creation wrapper for a concrete Drone."""

    def __init__(self, identifier: str, factory: Callable[[], Drone]) -> None:
        super().__init__(identifier)
        self._factory = factory
        self._real: Optional[Drone] = None

    def _ensure_realized(self) -> Drone:
        if self._real is None:
            self._real = self._factory()
        return self._real

    def capabilities(self) -> str:
        return self._ensure_realized().capabilities()

    def assign_mission(self, mission) -> None:  # type: ignore[override]
        self._ensure_realized().assign_mission(mission)

    def clear_mission(self) -> None:  # type: ignore[override]
        if self._real:
            self._real.clear_mission()

    @property
    def active_mission(self):  # type: ignore[override]
        return self._real.active_mission if self._real else None
