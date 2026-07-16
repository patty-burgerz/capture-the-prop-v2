from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from entities.weapons.travel.travel_behavior import TravelBehavior
from entities.weapons.impact.impact_behavior import ImpactBehavior

if TYPE_CHECKING:
    from entities.player import Player


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    owner_id: str
    damage: int

    travel_behavior: TravelBehavior
    impact_behaviors: tuple[ImpactBehavior, ...]

    ttl: float = 2.0
    alive: bool = True

    def update(self, world: Any, dt: float) -> None:
        if not self.alive:
            return

        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False
            return

        self.travel_behavior.update(self, world, dt)

    def impact(self, target: "Player") -> None:
        for impact_behavior in self.impact_behaviors:
            impact_behavior.apply(self, target)

        self.alive = False