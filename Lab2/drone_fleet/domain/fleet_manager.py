from typing import Optional, Dict, Callable
from drone_fleet.factory.drone_factory import (
    SurveyDroneFactory,
    CargoDroneFactory,
    CombatDroneFactory,
)
from drone_fleet.factory.drone_pool import DronePool
from drone_fleet.factory.mission_builder import MissionBuilder
from drone_fleet.models.drone import Drone
from drone_fleet.models.mission import Mission
from drone_fleet.utilities.adapters import LegacyMissionAdapter
from drone_fleet.utilities.decorators import StealthDecorator, RangeExtenderDecorator
from drone_fleet.utilities.proxy import DroneProxy


class FleetManager:
    """Facade + Singleton coordinating drone-related subsystems.

    Structural patterns exposed:
      - Facade: provides simple methods wrapping pooling, factories, builder.
      - Adapter: converts legacy mission dicts via `adapt_legacy_mission`.
      - Decorator: runtime capability augmentation via `enhance_drone`.
      - Proxy: lazy drone creation with `lazy_drone`.
    """

    _instance: Optional['FleetManager'] = None

    def __init__(self) -> None:
        if FleetManager._instance is not None:
            raise RuntimeError("Use FleetManager.instance() to get the singleton instance")
        self._pool = DronePool(max_size=5)
        # Map for lazy drone creation (proxy) by kind string
        self._lazy_factories: Dict[str, Callable[[str], Drone]] = {
            'survey': lambda ident: SurveyDroneFactory().create(ident),
            'cargo': lambda ident: CargoDroneFactory().create(ident),
            'combat': lambda ident: CombatDroneFactory().create(ident),
        }

    @classmethod
    def instance(cls) -> 'FleetManager':
        if cls._instance is None:
            cls._instance = FleetManager()
        return cls._instance

    def preload_drones(self) -> None:
        # Factory Method usage: concrete factories create specific drones
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

    # --- Adapter pattern convenience ---
    def adapt_legacy_mission(self, legacy_dict: dict) -> Mission:
        return LegacyMissionAdapter(legacy_dict).to_mission()

    # --- Proxy pattern convenience ---
    def lazy_drone(self, kind: str, identifier: str) -> Drone:
        factory = self._lazy_factories.get(kind.lower())
        if not factory:
            raise ValueError(f"Unknown drone kind: {kind}")
        return DroneProxy(identifier, lambda: factory(identifier))

    # --- Decorator pattern convenience ---
    def enhance_drone(self, drone: Drone, *, stealth: bool = False, range_extender: bool = False) -> Drone:
        if stealth:
            drone = StealthDecorator(drone)
        if range_extender:
            drone = RangeExtenderDecorator(drone)
        return drone
