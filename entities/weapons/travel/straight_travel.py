# entities/travel.py
from travel/travel_behavior import TravelBehavior

class StraightTravel(TravelBehavior):
    """Moves the bullet forward using velocity (units per second)."""

    def update(self, bullet, world, dt: float) -> None:
        bullet.x += bullet.vx * dt
        bullet.y += bullet.vy * dt
