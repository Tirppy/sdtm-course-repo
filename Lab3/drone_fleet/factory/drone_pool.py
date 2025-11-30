from typing import List, Optional
from drone_fleet.models.drone import Drone


class DronePool:
    """Holds reusable Drone instances and manages in-use tracking."""

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

    def checkout_specific(self, drone: Drone) -> Drone:
        """Checkout an explicitly chosen available drone."""
        if drone in self._available:
            self._available.remove(drone)
            self._in_use.append(drone)
            return drone
        raise RuntimeError("Requested drone is not available")

    @property
    def available_drones(self) -> List[Drone]:
        return list(self._available)

    @property
    def stats(self) -> str:
        return f"available={len(self._available)}, in_use={len(self._in_use)}"
