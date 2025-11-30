from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from drone_fleet.models.drone import Drone, SurveyDrone, CombatDrone
from drone_fleet.models.mission import Mission


class SelectionStrategy(ABC):
    """Defines the drone selection behavior.

    A strategy chooses one drone from the available pool for a mission.
    """

    @abstractmethod
    def select(self, available: List[Drone], mission: Mission) -> Drone:
        raise NotImplementedError


class SimpleSelectionStrategy(SelectionStrategy):
    """Takes the last available drone (LIFO)."""

    def select(self, available: List[Drone], mission: Mission) -> Drone:  # type: ignore[override]
        if not available:
            raise RuntimeError("No drones available")
        return available[-1]


class PrioritySelectionStrategy(SelectionStrategy):
    """Prefers certain drone types based on mission attributes.

    - High priority (>=4) -> prefer CombatDrone.
    - Payload contains 'Camera' -> prefer SurveyDrone.
    - Fallback to last available.
    """

    def select(self, available: List[Drone], mission: Mission) -> Drone:  # type: ignore[override]
        if not available:
            raise RuntimeError("No drones available")
        # Try priority rule
        if mission.priority >= 4:
            for d in available:
                if isinstance(d, CombatDrone):
                    return d
        # Try imaging rule
        payload = (mission.payload or "").lower()
        if "camera" in payload:
            for d in available:
                if isinstance(d, SurveyDrone):
                    return d
        return available[-1]
