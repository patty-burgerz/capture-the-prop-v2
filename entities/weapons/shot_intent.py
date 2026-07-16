from dataclasses import dataclass

from entities.weapons.impact.impact_behavior import ImpactBehavior
from entities.weapons.travel.travel_behavior import TravelBehavior


@dataclass(frozen=True)
class ShotIntent:
    name:str
    damage: int
    bullet_speed: float
    spread_deg: float
    travel_behavior: TravelBehavior
    impact_behaviors: tuple[ImpactBehavior, ...]