
from __future__ import annotations

from typing import TYPE_CHECKING

from entities.movement.movement_intent import MoveIntent

if TYPE_CHECKING:
    from core.game import Game
    from entities.player import Player


class MovementController:
    def __init__(self, game: "Game"):
        self.game = game

    def move(
        self,
        player: "Player",
        requested_position: tuple[float, float],
    ) -> bool:
        move_intent = MoveIntent(
            current_position=player.position,
            requested_position=requested_position,
        )

        final_intent = player.active_effects.modify_movement(move_intent)

        player.position = final_intent.requested_position
        return True