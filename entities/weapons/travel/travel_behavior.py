from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.bullet import Bullet


class TravelBehavior:
    """
    Strategy that controls how a bullet moves over time.
    """

    def update(self, bullet, world, dt: float) -> None:
        raise NotImplementedError("TravelBehavior subclasses must implement update()")