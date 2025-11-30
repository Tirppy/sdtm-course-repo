from abc import ABC, abstractmethod
from drone_fleet.models.drone import Drone, SurveyDrone, CargoDrone, CombatDrone


class DroneFactory(ABC):
    """Base factory interface for drone creation."""

    @abstractmethod
    def create(self, identifier: str) -> Drone:
        pass


class SurveyDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return SurveyDrone(identifier)


class CargoDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return CargoDrone(identifier)


class CombatDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return CombatDrone(identifier)
