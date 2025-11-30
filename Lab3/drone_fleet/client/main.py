from drone_fleet.domain.fleet_manager import FleetManager
from drone_fleet.utilities.strategies import PrioritySelectionStrategy


def demo():
    fm = FleetManager.instance()
    fm.preload_drones()
    print("Pool stats after preload:", fm.pool_stats())

    # Mission creation (helper builder kept from previous lab, comments trimmed)
    mission = (
        fm.create_mission("Survey Sector 7")
        .add_waypoint("WP-1")
        .add_waypoint("WP-2")
        .duration(30)
        .priority(2)
        .payload("HD Camera")
        .build()
    )
    print("Created mission:", mission)

    # Legacy mission adaptation (now just functional, no pattern mention)
    legacy = {"title": "Legacy Patrol", "wps": ["L1", "L2"], "len": 15, "prio": 4}
    adapted_mission = fm.adapt_legacy_mission(legacy)
    print("Adapted legacy mission:", adapted_mission)

    # Assign mission using current (simple) selection strategy
    drone = fm.assign_mission_to_drone(mission)
    print("Assigned", drone)
    print("Drone capabilities:", drone.capabilities())
    print("Pool stats after checkout:", fm.pool_stats())

    # Enhance drone capabilities dynamically
    enhanced = fm.enhance_drone(drone, stealth=True, range_extender=True)
    print("Enhanced drone capabilities:", enhanced.capabilities())

    fm.release_drone(drone)
    print("Released drone")
    print("Pool stats after release:", fm.pool_stats())

    # Lazy drone creation (instantiated only when needed)

    # Strategy pattern demonstration: switch to priority-based selection
    fm.set_selection_strategy(PrioritySelectionStrategy())
    high_priority_mission = (
        fm.create_mission("Urgent Recon")
        .add_waypoint("HP-1")
        .duration(10)
        .priority(5)
        .payload("Thermal Camera")
        .build()
    )
    chosen = fm.assign_mission_to_drone(high_priority_mission)
    print("High priority mission assigned to:", chosen)
    lazy = fm.lazy_drone("combat", "Lazy-X")
    print("Lazy drone created (proxy):", lazy)
    print("Lazy drone capabilities (triggers real creation):", lazy.capabilities())


if __name__ == "__main__":
    demo()
