from dataclasses import dataclass
from weapons/travel/straight_travel import StaightTravel
from weapons/travel/travel_behavior import TravelBehavior

@dataclass(frozen=True)
class GunSpec:
    name: str
    mag_size: int
    damage: int
    bullet_speed: float
    spread_deg: float = 0.0
    travel_behavior: TravelBehavior = StraightTravel()