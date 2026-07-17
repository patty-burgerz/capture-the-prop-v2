from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.bullet import Bullet
    from entities.player import Player


class ImpactBehavior:
    """
    Defines one effect that occurs when a bullet hits a target.
    """

    def apply(self, bullet: Bullet, target: Player) -> None:
        raise NotImplementedError