from drone_fleet.domain.fleet_manager import FleetManager


def demo():
    fm = FleetManager.instance()
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
    print("Created mission:", mission)

    drone = fm.assign_mission_to_drone(mission)
    print("Assigned", drone)
    print("Pool stats after checkout:", fm.pool_stats())

    fm.release_drone(drone)
    print("Released drone")
    print("Pool stats after release:", fm.pool_stats())


if __name__ == "__main__":
    demo()
