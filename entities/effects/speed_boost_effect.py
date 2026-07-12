"""
Speed boost effect.

This effect demonstrates movement effect functionality by multiplying
the displacement of movement.
"""

from entities.effects.active_effect import ActiveEffect


class SpeedBoostEffect(ActiveEffect):
    """
    Effect that increases movement speed.
    
    This is a movement effect that multiplies the displacement vector.
    Shot effects are unaffected.
    
    The current movement model passes position tuples (x, y) to modify_movement.
    This effect multiplies the displacement by a factor (default: 2.0).
    
    Since movement in _move_core is just position assignment, we interpret
    the "movement" as the delta from current position:
    - Input: new_position (x, y)
    - We multiply (x, y) by the speed_multiplier
    - Output: boosted_position
    """
    
    def __init__(self, speed_multiplier: float = 2.0):
        self.speed_multiplier = speed_multiplier
    
    def modify_movement(self, movement):
        """
        Boost movement by multiplying the position coordinates.
        
        In the current model where movement is just a new position tuple,
        we multiply the coordinates to simulate increased speed.
        """
        if isinstance(movement, tuple) and len(movement) == 2:
            x, y = movement
            return (x * self.speed_multiplier, y * self.speed_multiplier)
        return movement
