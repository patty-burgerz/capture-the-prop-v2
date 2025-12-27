# entities/Bullet.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol, Any


class TravelBehavior(Protocol):
    def step(self, bullet: "Bullet", world: Any, dt: float) -> None: ...


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    owner_id: str
    damage: int

    ttl: float = 2.0
    alive: bool = True
    travel: Optional[TravelBehavior] = None

    def update(self, world: Any, dt: float) -> None:
        if not self.alive:
            return

        self.ttl -= dt
        if self.ttl <= 0:
            self.alive = False
            return

        if self.travel is not None:
            self.travel.step(self, world, dt)
        else:
            self.x += self.vx * dt
            self.y += self.vy * dt
