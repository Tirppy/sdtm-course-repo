from drone_fleet.models.drone import Drone, SurveyDrone, CargoDrone, CombatDrone


class DroneFactory:
    """Factory Method for creating drones by type string."""

    @staticmethod
    def create(drone_type: str, identifier: str) -> Drone:
        t = drone_type.lower()
        if t == 'survey':
            return SurveyDrone(identifier)
        if t == 'cargo':
            return CargoDrone(identifier)
        if t == 'combat':
            return CombatDrone(identifier)
        raise ValueError(f"Unknown drone type: {drone_type}")
