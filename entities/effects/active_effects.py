"""
Container for active effects.

This container manages exactly two effect slots:
- shot: for modifying ShotIntent
- movement: for modifying movement data

At most one effect can be active per slot.
"""

from typing import Optional
from entities.effects.active_effect import ActiveEffect


class ActiveEffects:
    """
    Container for active effects with exactly two slots: shot and movement.
    
    Each slot can hold at most one active effect. If a slot is empty,
    the container returns the original object unchanged.
    
    This container is owned by Player and should be accessed only by Game
    during core mechanics execution.
    """
    
    def __init__(self):
        self._shot_effect: Optional[ActiveEffect] = None
        self._movement_effect: Optional[ActiveEffect] = None
    
    def set_shot_effect(self, effect: Optional[ActiveEffect]) -> None:
        """Assign or clear the active shot effect."""
        self._shot_effect = effect
    
    def set_movement_effect(self, effect: Optional[ActiveEffect]) -> None:
        """Assign or clear the active movement effect."""
        self._movement_effect = effect
    
    def get_shot_effect(self) -> Optional[ActiveEffect]:
        """Get the current shot effect, or None if empty."""
        return self._shot_effect
    
    def get_movement_effect(self) -> Optional[ActiveEffect]:
        """Get the current movement effect, or None if empty."""
        return self._movement_effect
    
    def modify_shot(self, shot_intent):
        """
        Apply the active shot effect to a ShotIntent.
        
        If no shot effect is active, returns the original shot_intent unchanged.
        """
        if self._shot_effect is None:
            return shot_intent
        return self._shot_effect.modify_shot(shot_intent)
    
    def modify_movement(self, movement):
        """
        Apply the active movement effect to movement data.
        
        If no movement effect is active, returns the original movement unchanged.
        """
        if self._movement_effect is None:
            return movement
        return self._movement_effect.modify_movement(movement)
