from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core.game import Game
    from entities.effects.active_effect import ActiveEffect


class EffectController:
    def __init__(self, game: "Game"):
        self.game = game

    def add_effect(self, player, effect):
        player.active_effects.add_effect(effect)
        return effect
