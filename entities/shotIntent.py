from dataclasses import dataclass
@dataclass(frozen = True)
class ShotIntent:
    weapon_name:str
    kind:str   # "projectile" (v1), later "hitscan"
    damage:int
    bullet_speed:float
    spread_deg:float


        