"""
Effects system for Capture the Prop v2.

Provides a typed, slot-based effect system with exactly two categories:
- shot: for modifying ShotIntent before Bullet creation
- movement: for modifying movement data before position update
"""

from entities.effects.active_effect import ActiveEffect
from entities.effects.active_effects import ActiveEffects
from entities.effects.double_damage_effect import DoubleDamageEffect
from entities.effects.speed_boost_effect import SpeedBoostEffect

__all__ = [
    "ActiveEffect",
    "ActiveEffects",
    "DoubleDamageEffect",
    "SpeedBoostEffect",
]
