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
from drone_fleet.utilities.observer import Observer


class FleetManager:
    """Singleton coordinator; emits Observer events for key actions."""

    _instance: Optional['FleetManager'] = None

    def __init__(self) -> None:
        if FleetManager._instance is not None:
            raise RuntimeError("Use FleetManager.instance()")
        self._pool = DronePool(max_size=5)
        self._lazy_factories: Dict[str, Callable[[str], Drone]] = {
            'survey': lambda ident: SurveyDroneFactory().create(ident),
            'cargo': lambda ident: CargoDroneFactory().create(ident),
            'combat': lambda ident: CombatDroneFactory().create(ident),
        }
        self._observers: list[Observer] = []

    @classmethod
    def instance(cls) -> 'FleetManager':
        if cls._instance is None:
            cls._instance = FleetManager()
        return cls._instance

    def register_observer(self, observer: Observer) -> None:
        self._observers.append(observer)

    def unregister_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify(self, event: str, **payload) -> None:
        for obs in list(self._observers):
            obs.update(event, payload)

    def preload_drones(self) -> None:
        drones = [
            SurveyDroneFactory().create('S-1'),
            CargoDroneFactory().create('C-1'),
            CombatDroneFactory().create('X-1'),
        ]
        self._pool.preload(drones)
        self._notify('pool.preloaded', size=len(drones))

    def create_mission(self, name: str) -> MissionBuilder:
        return MissionBuilder().name(name)

    def assign_mission_to_drone(self, mission: Mission) -> Drone:
        drone = self._pool.checkout()
        drone.assign_mission(mission)
        self._notify('mission.assigned', drone_id=drone.identifier, mission=mission)
        return drone

    def release_drone(self, drone: Drone) -> None:
        self._pool.release(drone)
        self._notify('drone.released', drone_id=drone.identifier)

    def pool_stats(self) -> str:
        return self._pool.stats

    def adapt_legacy_mission(self, legacy_dict: dict) -> Mission:
        mission = LegacyMissionAdapter(legacy_dict).to_mission()
        self._notify('mission.adapted', mission=mission)
        return mission

    def lazy_drone(self, kind: str, identifier: str) -> Drone:
        factory = self._lazy_factories.get(kind.lower())
        if not factory:
            raise ValueError(f"Unknown drone kind: {kind}")
        proxy = DroneProxy(identifier, lambda: factory(identifier))
        self._notify('proxy.created', drone_id=identifier, kind=kind)
        return proxy

    def enhance_drone(self, drone: Drone, *, stealth: bool = False, range_extender: bool = False) -> Drone:
        if stealth:
            drone = StealthDecorator(drone)
            self._notify('drone.decorated', type='stealth', drone_id=drone.identifier)
        if range_extender:
            drone = RangeExtenderDecorator(drone)
            self._notify('drone.decorated', type='range_extender', drone_id=drone.identifier)
        return drone
