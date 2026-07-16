from dataclasses import replace

from entities.weapons.shot_values.shot_value_modifier import (
    ShotValueModifier,
)


class DamageMultiplier(ShotValueModifier):
    def __init__(self, multiplier: float):
        self.multiplier = multiplier

    def modify(self, shot_intent):
        return replace(
            shot_intent,
            damage=shot_intent.damage * self.multiplier,
        )