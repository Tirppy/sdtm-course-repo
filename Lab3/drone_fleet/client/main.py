from drone_fleet.domain.fleet_manager import FleetManager
from drone_fleet.utilities.observer import ConsoleObserver, MissionCountObserver


def demo():
    fm = FleetManager.instance()

    # Attach observers (behavioral pattern demonstration)
    console = ConsoleObserver()
    counter = MissionCountObserver()
    fm.register_observer(console)
    fm.register_observer(counter)

    fm.preload_drones()
    print("Pool stats after preload:", fm.pool_stats())

    mission = (
        fm.create_mission("Survey Sector 7")
        .add_waypoint("WP-1")
        .add_waypoint("WP-2")
        .duration(30)
        .priority(2)
        .payload("HD Camera")
        .build()
    )
    print("Mission built:", mission)

    legacy = {"title": "Legacy Patrol", "wps": ["L1", "L2"], "len": 15, "prio": 4}
    adapted_mission = fm.adapt_legacy_mission(legacy)
    print("Legacy adapted:", adapted_mission)

    drone = fm.assign_mission_to_drone(mission)
    print("Assigned", drone)
    print("Capabilities:", drone.capabilities())
    print("Pool stats after checkout:", fm.pool_stats())

    enhanced = fm.enhance_drone(drone, stealth=True, range_extender=True)
    print("Enhanced capabilities:", enhanced.capabilities())

    fm.release_drone(drone)
    print("Pool stats after release:", fm.pool_stats())

    lazy = fm.lazy_drone("combat", "Lazy-X")
    print("Lazy proxy capabilities:", lazy.capabilities())

    print("Observer mission stats:", counter.stats())


if __name__ == "__main__":
    demo()
