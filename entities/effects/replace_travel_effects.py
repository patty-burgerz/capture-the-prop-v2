from dataclasses import replace

from entities.effects.active_effect import ShotTravelEffect
from entities.weapons.travel.travel_behavior import TravelBehavior


class ReplaceTravelEffect(ShotTravelEffect):
    def __init__(self, travel_behavior: TravelBehavior):
        self.travel_behavior = travel_behavior

    def modify_shot(self, shot_intent):
        return replace(
            shot_intent,
            travel_behavior=self.travel_behavior,
        )