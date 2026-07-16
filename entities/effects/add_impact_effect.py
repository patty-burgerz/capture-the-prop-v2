from dataclasses import replace

from entities.effects.active_effect import ShotImpactEffect
from entities.weapons.impact.impact_behavior import ImpactBehavior


class AddImpactEffect(ShotImpactEffect):
    def __init__(self, impact_behavior: ImpactBehavior):
        self.impact_behavior = impact_behavior

    def modify_shot(self, shot_intent):
        return replace(
            shot_intent,
            impact_behaviors=(
                *shot_intent.impact_behaviors,
                self.impact_behavior,
            ),
        )