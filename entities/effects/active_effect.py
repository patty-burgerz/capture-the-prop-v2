"""
Base class for all active effects.

An active effect is a temporary modification to player behavior.
- Shot effects modify ShotIntent before Bullet creation.
- Movement effects modify movement data before position update.

No effect should directly mutate Game or GameState.
"""


class ActiveEffect:
    """
    Base class for all active effects.
    
    Each effect has at most one instance active per slot (shot or movement).
    Effects are immutable in the sense that they do not mutate the entities
    they transform; instead, they return new/modified values.
    """
    
    def modify_shot(self, shot_intent):
        """
        Transform a ShotIntent.
        
        Args:
            shot_intent: ShotIntent to modify
            
        Returns:
            Modified ShotIntent (or the same if no modification)
        """
        return shot_intent
    
    def modify_movement(self, movement):
        """
        Transform movement data.
        
        Args:
            movement: Movement data (typically a tuple (x, y) for position,
                     or a dict with movement parameters)
            
        Returns:
            Modified movement data (or the same if no modification)
        """
        return movement
