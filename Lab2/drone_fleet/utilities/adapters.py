from typing import Dict, Any
from drone_fleet.factory.mission_builder import MissionBuilder
from drone_fleet.models.mission import Mission


class LegacyMissionAdapter:
    """Adapter pattern: adapts a legacy mission dictionary format to `Mission`.

    Expected legacy keys:
      - title: str -> mission name
      - wps: list[str] -> waypoints
      - len: int (minutes) -> duration
      - prio: int -> priority (optional)
      - cargo: str -> payload (optional)
    """

    def __init__(self, legacy_data: Dict[str, Any]) -> None:
        self._data = legacy_data

    def to_mission(self) -> Mission:
        builder = MissionBuilder().name(self._data.get("title", "Unnamed"))
        for wp in self._data.get("wps", []):
            builder.add_waypoint(wp)
        duration = int(self._data.get("len", 0))
        prio = int(self._data.get("prio", 3))
        cargo = self._data.get("cargo")
        builder.duration(duration).priority(prio)
        if cargo:
            builder.payload(cargo)
        return builder.build()
