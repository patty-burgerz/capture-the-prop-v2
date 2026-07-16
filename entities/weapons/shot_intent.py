from dataclasses import dataclass
from entities.weapons.gun_spec import GunSpec
from travel/travel_behavior import TravelBehavior
from impact/impact_behavior import ImpactBehavior
@dataclass(frozen=True)
class ShotIntent:
    """
    Represents one trigger pull.

    Values here are copied from the weapon's GunSpec when the shot is fired.
    This is intentional.

    GunSpec holds the default stats for a weapon.
    ShotIntent holds the final values used for THIS shot, so powerups,
    debuffs, or special effects can modify them without changing the weapon
    itself.

    Once a ShotIntent exists, game systems should use these values and not
    read from GunSpec.
    """
    spec: GunSpec
    damage: int
    bullet_speed: float
    spread_deg: float,
    travel_behavior: TravelBehavior,
    impact_behaviors: tuple[ImpactBehavior, ...]