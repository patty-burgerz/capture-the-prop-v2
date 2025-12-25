from entities.weapons.gun_spec import GunSpec

# Canonical weapon definitions used across the game
GLOCK_17 = GunSpec(
    name="Glock 17",
    mag_size=17,
    damage=22,
    bullet_speed=30.0,
    spread_deg=2.0,
)

AR_15 = GunSpec(
    name="AR-15",
    mag_size=30,
    damage=30,
    bullet_speed=45.0,
    spread_deg=1.2,
)
