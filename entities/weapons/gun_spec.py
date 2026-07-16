from dataclasses import dataclass, field

from entities.weapons.travel.straight_travel import StraightTravel
from entities.weapons.travel.travel_behavior import TravelBehavior
from entities.weapons.impact.damage_impact import DamageImpact
from entities.weapons.impact.impact_behavior import ImpactBehavior


@dataclass(frozen=True)
class GunSpec:
    name: str
    damage: int
    bullet_speed: float
    spread_deg: float

    travel_behavior: TravelBehavior = field(
        default_factory=StraightTravel
    )

    impact_behaviors: tuple[ImpactBehavior, ...] = field(
        default_factory=lambda: (DamageImpact(),)
    )