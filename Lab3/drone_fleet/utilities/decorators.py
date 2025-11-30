from abc import ABC
from drone_fleet.models.drone import Drone


class DroneDecorator(Drone, ABC):
    """Wraps a drone to extend capabilities at runtime."""

    def __init__(self, wrapped: Drone) -> None:  # type: ignore[override]
        super().__init__(wrapped.identifier)
        self._wrapped = wrapped

    def assign_mission(self, mission) -> None:  # delegate
        self._wrapped.assign_mission(mission)

    def clear_mission(self) -> None:
        self._wrapped.clear_mission()

    @property
    def active_mission(self):  # type: ignore[override]
        return self._wrapped.active_mission


class StealthDecorator(DroneDecorator):
    def capabilities(self) -> str:
        return self._wrapped.capabilities() + " + low-visibility stealth"


class RangeExtenderDecorator(DroneDecorator):
    def capabilities(self) -> str:
        return self._wrapped.capabilities() + " + extended flight range"
