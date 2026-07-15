from dataclasses import replace

from entities.effects.active_effect import ActiveEffect
from entities.movement.movement_intent import MoveIntent


class SpeedBoostEffect(ActiveEffect):
    def __init__(self, speed_multiplier: float = 2.0):
        self.speed_multiplier = speed_multiplier

    def modify_movement(self, move_intent: MoveIntent) -> MoveIntent:
        current_x, current_y = move_intent.current_position
        requested_x, requested_y = move_intent.requested_position

        dx = requested_x - current_x
        dy = requested_y - current_y

        boosted_position = (
            current_x + dx * self.speed_multiplier,
            current_y + dy * self.speed_multiplier,
        )

        return replace(
            move_intent,
            requested_position=boosted_position,
        )