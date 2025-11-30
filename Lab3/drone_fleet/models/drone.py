from __future__ import annotations
from abc import ABC, abstractmethod


class Drone(ABC):
    """Base drone abstraction."""

    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
        self._mission = None

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def active_mission(self):
        return self._mission

    def assign_mission(self, mission) -> None:
        self._mission = mission

    def clear_mission(self) -> None:
        self._mission = None

    @abstractmethod
    def capabilities(self) -> str:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._identifier}, mission={self._mission})"


class SurveyDrone(Drone):
    def capabilities(self) -> str:
        return "High-resolution imaging and terrain mapping"


class CargoDrone(Drone):
    def capabilities(self) -> str:
        return "Medium payload transport"


class CombatDrone(Drone):
    def capabilities(self) -> str:
        return "Defensive countermeasures and target tracking"
