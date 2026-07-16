from __future__ import annotations

from typing import TYPE_CHECKING

from entities.weapons.impact.impact_behavior import ImpactBehavior

if TYPE_CHECKING:
    from entities.Bullet import Bullet
    from entities.player import Player


class YeetImpact(ImpactBehavior):
    def __init__(self, yeet_multiplier: float = 1.0):
        self.yeet_multiplier = yeet_multiplier

    def apply(self, bullet: "Bullet", target: "Player") -> None:
        yeet_strength = bullet.damage * self.yeet_multiplier

        # Temporary proof that the impact executed.
        # Replace this later with vertical velocity / knockback.
        target.update(f"BONK! Yeet strength: {yeet_strength}")