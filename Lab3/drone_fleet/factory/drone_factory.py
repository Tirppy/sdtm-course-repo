from abc import ABC, abstractmethod
from drone_fleet.models.drone import Drone, SurveyDrone, CargoDrone, CombatDrone


class DroneFactory(ABC):
    """Creates drone instances of a specific type."""

    @abstractmethod
    def create(self, identifier: str) -> Drone:
        raise NotImplementedError


class SurveyDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return SurveyDrone(identifier)


class CargoDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return CargoDrone(identifier)


class CombatDroneFactory(DroneFactory):
    def create(self, identifier: str) -> Drone:
        return CombatDrone(identifier)
