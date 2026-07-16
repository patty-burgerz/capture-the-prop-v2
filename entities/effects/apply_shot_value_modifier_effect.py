from entities.effects.active_effect import ShotValueEffect
from entities.weapons.shot_values.shot_value_modifier import (
    ShotValueModifier,
)


class ApplyShotValueModifierEffect(ShotValueEffect):
    def __init__(self, modifier: ShotValueModifier):
        self.modifier = modifier

    def modify_shot(self, shot_intent):
        return self.modifier.modify(shot_intent)