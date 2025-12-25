from dataclasses import dataclass

@dataclass(frozen=True)
class GunSpec:
    name: str
    mag_size: int
    damage: int
    bullet_speed: float
    spread_deg: float = 0.0
    kind: str = "projectile"   # future: "hitscan"