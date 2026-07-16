from entities.effects.active_effect import MovementEffect
from entities.movement.modifiers.movement_modifier import (
    MovementModifier,
)


class ApplyMovementModifierEffect(MovementEffect):
    def __init__(self, modifier: MovementModifier):
        self.modifier = modifier

    def modify_movement(self, move_intent):
        return self.modifier.modify(move_intent)