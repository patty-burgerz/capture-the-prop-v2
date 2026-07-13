from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.game import Game


class WorldController:
    def __init__(self, game: "Game"):
        self.game = game

    def update(self, dt: float) -> None:
        for bullet in self.game.bullets:
            bullet.update(self.game, dt)

        self.game.bullets = [b for b in self.game.bullets if b.alive]
