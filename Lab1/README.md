# Autonomous Drone Fleet – Creational Design Patterns Lab

## 1. Topic & Objectives
This lab explores several Creational Design Patterns in a compact Python domain: **Autonomous Drone Fleet Management**. The goal is to show how different object creation concerns map naturally to patterns that control, simplify, or optimize instantiation.

Objectives covered:
- Study and apply Creational Design Patterns.
- Define a small but interesting domain (drone fleet) with its core entities.
- Use at least three creational patterns in a working sample project.

Implemented Patterns (4 total):
1. Builder – for assembling complex `Mission` objects.
2. Factory Method – for creating specific drone types via `DroneFactory`.
3. Object Pool – for reusing `Drone` instances in `DronePool`.
4. Singleton – for global coordination in `FleetManager`.

## 2. Domain Overview
An autonomous fleet executes missions composed of waypoints, duration, and optional payloads. Drones have specialized capabilities (survey imaging, cargo transport, combat support). Efficient creation and reuse of these objects mirrors real-world constraints (expensive initialization, consistent configuration, central coordination).

### Core Entities
- `Mission` – Immutable description of a task (name, waypoints, duration, priority, payload).
- `Drone` (abstract) – Base for all drones; tracks an assigned mission.
  - `SurveyDrone`, `CargoDrone`, `CombatDrone` – Concrete specializations.
- `FleetManager` – Singleton providing a single orchestration point.
- `MissionBuilder` – Fluent builder for `Mission`.
- `DroneFactory` – Selects concrete drone subclass by a type string.
- `DronePool` – Manages available vs. in-use drones (Object Pool).

## 3. Pattern Rationale & Mapping
| Pattern | Applied To | Why | Key Benefit |
|---------|------------|-----|-------------|
| Builder | `MissionBuilder` -> `Mission` | Missions have multiple optional attributes and collections (waypoints). | Readable, safe, incremental construction; avoids telescoping constructors. |
| Factory Method | `DroneFactory.create(type, id)` | Different drone types chosen at runtime. | Centralizes type selection logic; isolates creation code from callers. |
| Object Pool | `DronePool` | Drones assumed expensive to create; reuse desirable. | Controls lifecycle, reduces repeated instantiation. |
| Singleton | `FleetManager.instance()` | One global coordinator needed. | Guarantees single access point to pool & builders. |

## 4. Directory / Package Structure
```
Lab1/
  README.md
  drone_fleet/
    __init__.py
    client/
      __init__.py
      main.py          # Demo script
    domain/
      __init__.py
      fleet_manager.py # Singleton orchestrator
    factory/
      __init__.py
      mission_builder.py
      drone_factory.py
      drone_pool.py
    models/
      __init__.py
      mission.py       # Immutable Mission model
      drone.py         # Drone hierarchy
```
Packages loosely group responsibilities: `models` (data), `factory` (creation logic), `domain` (orchestration), `client` (demo/app entry point).

## 5. Creation Flows
### Mission Creation (Builder)
1. Request a builder from `FleetManager.create_mission(name)`.
2. Chain: add waypoints, set duration/priority/payload.
3. Call `.build()` – validates required fields and returns immutable `Mission`.

### Drone Creation (Factory Method)
1. `DroneFactory.create('survey', 'S-1')` chooses `SurveyDrone`.
2. Centralizes mapping of type strings to concrete classes.

### Drone Reuse (Object Pool)
1. `FleetManager.preload_drones()` seeds the pool.
2. `assign_mission_to_drone(mission)` checks out a drone; mission assigned.
3. After use: `release_drone(drone)` clears mission and returns it to availability.

### Coordination (Singleton)
`FleetManager.instance()` ensures only one instance manages pool and mission builders. Direct constructor use is blocked to enforce pattern.

## 6. Example Usage (Demo Script)
Run the demo from inside `Lab1` directory:
```bash
python -m drone_fleet.client.main
```
Output (approximate):
```
Pool stats after preload: available=3, in_use=0
Created mission: Mission(name='Survey Sector 7', waypoints=['WP-1', 'WP-2'], duration_minutes=30, priority=2, payload='HD Camera')
Assigned SurveyDrone(id=S-1, mission=Mission(...))
Pool stats after checkout: available=2, in_use=1
Released drone
Pool stats after release: available=3, in_use=0
```

## 7. Design Notes & Simplicity Choices
- Minimal error handling—only validates essential mission fields.
- No external libraries or frameworks; pure Python standard features.
- Single-threaded assumption; pool not synchronized. (Thread-safety would require locks.)
- `Mission` treated as immutable by exposing copies of waypoint list.
- Identifiers are simple strings; no UUID generation to keep code short.

## 8. Extensibility Ideas (Beyond Scope)
- Add Prototype pattern via cloning pre-configured drone templates.
- Introduce configuration file for initial pool size and drone mix.
- Add simple telemetry logging strategy or observer for mission lifecycle.
- Make pool blocking with wait/notify for high contention scenarios.

## 9. Evaluation Mapping
Requirement | Where Satisfied
----------- | ----------------
Domain defined | Drone fleet entities (`mission.py`, `drone.py`)
At least 3 creational patterns | Builder, Factory Method, Object Pool (+ Singleton extra)
Separation into packages | `client`, `domain`, `factory`, `models`
Instantiation mechanisms documented | Sections 3–6 above
Working sample project | `main.py` demo creates and uses objects via patterns

## 10. Quick Pattern Cheat-Sheet
- Builder: Separate construction from representation; chain methods to assemble; final `build()` enforces validity.
- Factory Method: Encapsulate selection logic so callers don't depend on concrete classes; enables future expansion (e.g., add `StealthDrone`).
- Object Pool: Manage reusable instances; reduce creation overhead; track available vs. in-use state.
- Singleton: Ensure a single coordinator instance; centralize access to shared resources.

## 11. Running & Resetting
Re-run the demo anytime; pool is recreated fresh on interpreter start. To experiment, modify `FleetManager.preload_drones()` or adjust `DronePool(max_size=...)`.

---
**End of Report** – Concise, pattern-focused implementation ready for lab evaluation.
