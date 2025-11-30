from typing import List
from drone_fleet.models.drone import Drone


class DronePool:
    """Fixed-size pool managing reusable Drone instances."""

    def __init__(self, max_size: int) -> None:
        self._available: List[Drone] = []
        self._in_use: List[Drone] = []
        self._max_size = max_size

    def preload(self, drones: List[Drone]) -> None:
        for d in drones:
            if len(self._available) + len(self._in_use) < self._max_size:
                self._available.append(d)

    def checkout(self) -> Drone:
        if self._available:
            d = self._available.pop()
            self._in_use.append(d)
            return d
        raise RuntimeError("No available drones in pool")

    def release(self, drone: Drone) -> None:
        if drone in self._in_use:
            drone.clear_mission()
            self._in_use.remove(drone)
            self._available.append(drone)

    @property
    def stats(self) -> str:
        return f"available={len(self._available)}, in_use={len(self._in_use)}"
