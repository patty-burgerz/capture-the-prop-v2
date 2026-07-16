from entities.weapons.travel.travel_behavior import TravelBehavior


class StraightTravel(TravelBehavior):
    def update(self, bullet, world, dt: float) -> None:
        bullet.x += bullet.vx * dt
        bullet.y += bullet.vy * dt