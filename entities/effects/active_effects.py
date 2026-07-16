from entities.effects.active_effect import (
    ActiveEffect,
    MovementEffect,
    ShotImpactEffect,
    ShotTravelEffect,
    ShotValueEffect,
)


class ActiveEffects:
    def __init__(self):
        self._shot_value_effects: dict[type, ShotValueEffect] = {}
        self._shot_travel_effect: ShotTravelEffect | None = None
        self._shot_impact_effects: dict[type, ShotImpactEffect] = {}
        self._movement_effects: dict[type, MovementEffect] = {}

    def add_effect(self, effect: ActiveEffect) -> None:
        if isinstance(effect, ShotValueEffect):
            self._shot_value_effects[self._effect_key(effect)] = effect
            return

        if isinstance(effect, ShotTravelEffect):
            self._shot_travel_effect = effect
            return

        if isinstance(effect, ShotImpactEffect):
            self._shot_impact_effects[self._effect_key(effect)] = effect
            return

        if isinstance(effect, MovementEffect):
            self._movement_effects[self._effect_key(effect)] = effect
            return

        raise TypeError(
            f"Unsupported active effect: {type(effect).__name__}"
        )


    def modify_shot(self, shot_intent):
        final_intent = shot_intent

        for effect in self._shot_value_effects.values():
            final_intent = effect.modify_shot(final_intent)

        if self._shot_travel_effect is not None:
            final_intent = self._shot_travel_effect.modify_shot(
                final_intent
            )

        for effect in self._shot_impact_effects.values():
            final_intent = effect.modify_shot(final_intent)

        return final_intent

    def modify_movement(self, move_intent):
        final_intent = move_intent

        for effect in self._movement_effects.values():
            final_intent = effect.modify_movement(final_intent)

        return final_intent

    @staticmethod
    def _effect_key(effect: ActiveEffect):
        inner_object = getattr(effect, "modifier", None)

        if inner_object is None:
            inner_object = getattr(effect, "impact_behavior", None)

        return type(inner_object) if inner_object is not None else type(effect)