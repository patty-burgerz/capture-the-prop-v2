# entities/travel.py

class StraightTravel:
    """Moves the bullet forward using velocity (units per second)."""

    def step(self, bullet, world, dt: float) -> None:
        bullet.x += bullet.vx * dt
        bullet.y += bullet.vy * dt
