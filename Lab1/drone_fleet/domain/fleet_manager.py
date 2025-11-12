from typing import Optional
from drone_fleet.factory.drone_factory import (
    SurveyDroneFactory,
    CargoDroneFactory,
    CombatDroneFactory,
)
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
        # Use classical GoF Factory Method: concrete factories create specific drones
        drones = [
            SurveyDroneFactory().create('S-1'),
            CargoDroneFactory().create('C-1'),
            CombatDroneFactory().create('X-1'),
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
