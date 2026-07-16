class ActiveEffect:
    """Base type for temporary player effects."""


class ShotValueEffect(ActiveEffect):
    def modify_shot(self, shot_intent):
        return shot_intent


class ShotTravelEffect(ActiveEffect):
    def modify_shot(self, shot_intent):
        return shot_intent


class ShotImpactEffect(ActiveEffect):
    def modify_shot(self, shot_intent):
        return shot_intent


class MovementEffect(ActiveEffect):
    def modify_movement(self, move_intent):
        return move_intent