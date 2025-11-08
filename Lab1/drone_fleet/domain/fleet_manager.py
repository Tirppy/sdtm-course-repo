from typing import Optional
from drone_fleet.factory.drone_factory import DroneFactory
from drone_fleet.factory.drone_pool import DronePool
from drone_fleet.factory.mission_builder import MissionBuilder
from drone_fleet.models.drone import Drone
from drone_fleet.models.mission import Mission


class FleetManager:
    """Singleton coordinating drone creation and pooling."""

    _instance: Optional['FleetManager'] = None

    def __init__(self) -> None:
        if FleetManager._instance is not None:
            raise RuntimeError("Use FleetManager.instance() to get the singleton instance")
        self._pool = DronePool(max_size=5)

    @classmethod
    def instance(cls) -> 'FleetManager':
        if cls._instance is None:
            cls._instance = FleetManager()
        return cls._instance

    def preload_drones(self) -> None:
        drones = [
            DroneFactory.create('survey', 'S-1'),
            DroneFactory.create('cargo', 'C-1'),
            DroneFactory.create('combat', 'X-1')
        ]
        self._pool.preload(drones)

    def create_mission(self, name: str) -> MissionBuilder:
        return MissionBuilder().name(name)

    def assign_mission_to_drone(self, mission: Mission) -> Drone:
        drone = self._pool.checkout()
        drone.assign_mission(mission)
        return drone

    def release_drone(self, drone: Drone) -> None:
        self._pool.release(drone)

    def pool_stats(self) -> str:
        return self._pool.stats
