from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.game import Game
    from entities.effects.active_effect import ActiveEffect


class EffectController:
    def __init__(self, game: "Game"):
        self.game = game

    def set_shot_effect(self, player, effect: Optional["ActiveEffect"]):
        player.active_effects.set_shot_effect(effect)
        return True

    def set_movement_effect(self, player, effect: Optional["ActiveEffect"]):
        player.active_effects.set_movement_effect(effect)
        return True
