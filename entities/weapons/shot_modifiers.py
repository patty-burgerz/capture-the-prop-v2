from dataclasses import replace

from entities.weapons.shot_intent import ShotIntent


class DoubleDamageModifier:
    def apply(self, shot: ShotIntent) -> ShotIntent:
        new_shot=replace(
            shot,
            damage=shot.damage * 2,
        )
        return new_shot
