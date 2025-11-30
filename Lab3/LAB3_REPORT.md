# Laboratory 3 Report

**Topic:** Behavioral Design Patterns (Observer Integration)
**Author:** (Add your name here)

## 1. Introduction / Motivation
This lab extends the existing drone fleet management system by introducing a behavioral design pattern to improve decoupled communication between components. The previously implemented structural patterns (factories, builder, proxy, decorators, pooling, singleton) provided object creation and composition flexibility. For dynamic runtime reactions (e.g., logging, metrics), a behavioral approach is needed.

## 2. Chosen Pattern: Observer
The Observer pattern enables interested parties (observers) to subscribe to events emitted by a subject. Here, `FleetManager` acts as the subject, notifying observers about mission lifecycle and drone pool changes. This avoids hard-coded logging or metric hooks inside core business logic and supports easy extension.

### Why Observer?
- Minimal intrusion into existing code.
- Clear event points (mission adapted, assigned, drone released, pool preload, proxy created, decorations applied).
- Enables multiple independent listeners (console logging, mission counting) without modifying core flow.

## 3. Implementation Overview
- Subject: `FleetManager` (in `drone_fleet/domain/fleet_manager.py`).
  - Maintains a list of `Observer` instances.
  - Emits events via `_notify(event, **payload)` at key operations.
- Observer Interface: `Observer` (in `drone_fleet/utilities/observer.py`).
  - Defines `update(event: str, payload: dict)`.
- Concrete Observers:
  - `ConsoleObserver` – prints each event.
  - `MissionCountObserver` – tracks counts of created/adapted and assigned missions for simple metrics.
- Demo Integration: Updated client demo in `drone_fleet/client/main.py` registers observers and prints final stats.

## 4. Key Code Snippets
### FleetManager Subject (excerpt)
```python
self._observers: list[Observer] = []
...
def _notify(self, event: str, **payload) -> None:
    for obs in list(self._observers):
        obs.update(event, payload)
```
### Emitting an Event
```python
def assign_mission_to_drone(self, mission: Mission) -> Drone:
    drone = self._pool.checkout()
    drone.assign_mission(mission)
    self._notify('mission.assigned', drone_id=drone.identifier, mission=mission)
    return drone
```
### Observer Implementation
```python
class MissionCountObserver(Observer):
    def __init__(self) -> None:
        self.created = 0
        self.assigned = 0
    def update(self, event: str, payload: Dict[str, Any]) -> None:
        if event in {"mission.adapted"}:
            self.created += 1
        if event == "mission.assigned":
            self.assigned += 1
```
### Client Demo Registration
```python
console = ConsoleObserver()
counter = MissionCountObserver()
fm.register_observer(console)
fm.register_observer(counter)
```

## 5. Event List
- `pool.preloaded` – drones added to pool.
- `mission.adapted` – legacy mission dictionary converted.
- `mission.assigned` – mission bound to a drone.
- `drone.released` – drone returned to pool.
- `proxy.created` – lazy proxy instantiated.
- `drone.decorated` – capability enhancement applied.

## 6. Results
Running the demo produces observer output for each event and final mission statistics:
```
[OBS] mission.assigned -> {...}
Observer mission stats: missions_created=1, missions_assigned=1
```
This validates decoupled runtime monitoring without altering existing logic paths outside of event hooks.

## 7. Conclusions
The Observer pattern cleanly augments the drone fleet system with extensible runtime reactions. New observers (e.g., persistence, alerting, analytics) can be added without modifying domain logic. This satisfies the lab requirement of integrating a behavioral pattern while keeping complexity low.

## 8. Future Extensions (Optional)
- Add filtering observers (subscribe only to certain events).
- Introduce asynchronous dispatch for non-blocking notifications.
- Implement Strategy pattern for drone selection based on mission priority.
