# Structural Design Patterns in Drone Fleet System

Author: Your Name Here

## 1. Introduction & Motivation
This laboratory extends the existing drone fleet management system by incorporating three (actually four) structural design patterns to improve flexibility and clarity of composition: Facade, Adapter, Decorator, and Proxy. These patterns simplify integration of legacy data, runtime capability changes, and resource management while keeping the public API small (a single client script) and code complexity low.

## 2. Implemented Patterns

### Facade
Location: `drone_fleet/domain/fleet_manager.py` (`FleetManager` class).
The fleet manager already coordinated factories, pool, and builders; we formalized its role as a Facade by adding convenience methods for new structural patterns, centralizing subsystem access.

### Adapter
Location: `drone_fleet/utilities/adapters.py` (`LegacyMissionAdapter`).
Adapts a legacy dict format (keys: `title`, `wps`, `len`, `prio`, `cargo`) into a strongly-typed `Mission` using the existing Builder. This allows integrating external or older data sources without changing domain models.

### Decorator
Location: `drone_fleet/utilities/decorators.py` (`DroneDecorator`, `StealthDecorator`, `RangeExtenderDecorator`).
Wraps a `Drone` at runtime to append capability descriptions (e.g., stealth, extended range) without subclass explosion or modifying original classes. Demonstrated when enhancing a checked-out drone.

### Proxy
Location: `drone_fleet/utilities/proxy.py` (`DroneProxy`).
Provides lazy instantiation of concrete drones using a factory callable. Creation cost is deferred until the first capability or mission assignment is requested.

## 3. Code Snippets & Explanations

#### Adapter Usage
Client snippet (`client/main.py`):
```python
legacy = {"title": "Legacy Patrol", "wps": ["L1", "L2"], "len": 15, "prio": 4}
adapted_mission = fm.adapt_legacy_mission(legacy)
```
The adapter isolates translation logic, keeping domain models clean.

#### Decorator Usage
```python
enhanced = fm.enhance_drone(drone, stealth=True, range_extender=True)
print(enhanced.capabilities())
```
Multiple decorators compose; each augments `capabilities()` output transparently.

#### Proxy Usage
```python
lazy = fm.lazy_drone("combat", "Lazy-X")
print(lazy.capabilities())  # triggers real creation
```
The proxy postpones resource allocation, helpful for tentative planning scenarios.

## 4. Results
Running the demo (`python -m drone_fleet.client.main`) produces output illustrating:
1. Pool preload and stats.
2. Builder-created mission & adapted legacy mission.
3. Drone assignment and capability enhancement via decorators.
4. Lazy (proxy) drone capability resolution.

## 5. Conclusions
The introduced structural patterns integrate smoothly with existing creational patterns (Factory Method, Builder, Singleton). The Facade keeps the client simple; Adapter bridges legacy data; Decorator enables dynamic augmentation; Proxy optimizes deferred creation. The changes remain minimal and localized, preserving project simplicity while satisfying laboratory objectives.

---
Potential Next Steps (optional): Composite pattern for grouping missions; Flyweight for shared telemetry objects if scalability demands.
