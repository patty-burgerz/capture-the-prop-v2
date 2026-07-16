from dataclasses import replace

from entities.movement.movement_intent import MoveIntent
from entities.movement.modifiers.movement_modifier import (
    MovementModifier,
)


class SpeedMultiplier(MovementModifier):
    def __init__(self, multiplier: float):
        self.multiplier = multiplier

    def modify(self, move_intent: MoveIntent) -> MoveIntent:
        current_x, current_y = move_intent.current_position
        requested_x, requested_y = move_intent.requested_position

        dx = requested_x - current_x
        dy = requested_y - current_y

        return replace(
            move_intent,
            requested_position=(
                current_x + dx * self.multiplier,
                current_y + dy * self.multiplier,
            ),
        )