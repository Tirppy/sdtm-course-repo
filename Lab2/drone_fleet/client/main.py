from drone_fleet.domain.fleet_manager import FleetManager


def demo():
    fm = FleetManager.instance()
    fm.preload_drones()
    print("Pool stats after preload:", fm.pool_stats())

    # Builder (existing) + Facade usage
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

    # Adapter pattern demonstration (legacy dict -> Mission)
    legacy = {"title": "Legacy Patrol", "wps": ["L1", "L2"], "len": 15, "prio": 4}
    adapted_mission = fm.adapt_legacy_mission(legacy)
    print("Adapted legacy mission:", adapted_mission)

    # Checkout and assign mission
    drone = fm.assign_mission_to_drone(mission)
    print("Assigned", drone)
    print("Drone capabilities:", drone.capabilities())
    print("Pool stats after checkout:", fm.pool_stats())

    # Decorator pattern: enhance drone with stealth + range
    enhanced = fm.enhance_drone(drone, stealth=True, range_extender=True)
    print("Enhanced drone capabilities:", enhanced.capabilities())

    fm.release_drone(drone)
    print("Released drone")
    print("Pool stats after release:", fm.pool_stats())

    # Proxy pattern: create lazy drone (won't instantiate until capabilities called)
    lazy = fm.lazy_drone("combat", "Lazy-X")
    print("Lazy drone created (proxy):", lazy)
    print("Lazy drone capabilities (triggers real creation):", lazy.capabilities())


if __name__ == "__main__":
    demo()
