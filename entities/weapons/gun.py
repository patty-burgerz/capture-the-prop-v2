# gun.py
#
# Concrete firearm implementation.
#
# Design notes (important):
# - Gun is a Weapon subclass. It owns *weapon mechanics* (ammo) and uses GunSpec for defaults.
# - Gun.use() does NOT spawn bullets, apply damage, check match phase, or print.
# - Gun.use() returns a ShotIntent (a per-shot "receipt") or None if the gun can't fire.
#
# Ownership:
# - self.owner is assigned/cleared by the Game core on pickup/drop.
# - Gun never assigns ownership itself.

from __future__ import annotations
import inspect

from typing import Optional

from .weapon import Weapon
from .gun_spec import GunSpec
from .shot_intent import ShotIntent


class Gun(Weapon):
    """
    Generic firearm.

    Runtime state:
    - ammo: mutable, per-instance (two Glocks can have different ammo)

    Defaults:
    - spec: immutable recipe shared across instances
    """

    def __init__(self, spec: GunSpec, starting_ammo: Optional[int] = None):
        super().__init__(name=spec.name)
        self.spec = spec

        # If starting_ammo isn't provided, start full.
        # Clamp to [0, mag_size] to avoid nonsense values.
        if starting_ammo is None:
            self.ammo = spec.mag_size
        else:
            self.ammo = max(0, min(starting_ammo, spec.mag_size))

    def has_ammo(self) -> bool:
        return self.ammo > 0

    def reload(self) -> None:
        self.ammo = self.spec.mag_size

    def use(self) -> Optional[ShotIntent]:
        """
        Attempt to fire.

        Returns:
            ShotIntent if the shot is allowed by weapon mechanics (owner + ammo)
            None otherwise.

        Note:
            Authorization (stunned, match phase, blanks vs real) is NOT handled here.
            That is handled by Game + State. This method only handles gun mechanics.
        """
        if self.owner is None:
            return None

        if not self.has_ammo():
            return None

        # Consume ammo as part of weapon mechanics.
        self.ammo -= 1

        # Create a per-shot receipt (copied from spec so it can be modified per-shot
        # without mutating the shared GunSpec).
        return ShotIntent(
            spec=self.spec,
            damage=self.spec.damage,
            bullet_speed=self.spec.bullet_speed,
            spread_deg=self.spec.spread_deg,
        )
