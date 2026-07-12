"""
Double damage effect.

This effect doubles the damage of all shots while active.
It replaces the previous DoubleDamageModifier.
"""

from dataclasses import replace
from entities.effects.active_effect import ActiveEffect


class DoubleDamageEffect(ActiveEffect):
    """
    Effect that doubles the damage of all shots.
    
    This is a shot effect that modifies the damage field of ShotIntent.
    Movement is unaffected.
    """
    
    def modify_shot(self, shot_intent):
        """
        Double the damage of the shot.
        
        Uses dataclasses.replace to preserve immutability of ShotIntent.
        """
        return replace(
            shot_intent,
            damage=shot_intent.damage * 2,
        )
