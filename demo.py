from core.game import Game
from entities.player import Player

from entities.effects.apply_movement_modifier_effect import (
    ApplyMovementModifierEffect,
)
from entities.effects.apply_shot_value_modifier_effect import (
    ApplyShotValueModifierEffect,
)

from entities.movement.modifiers.speed_multiplier import (
    SpeedMultiplier,
)
from entities.weapons.shot_values.damage_multiplier import (
    DamageMultiplier,
)

from entities.weapons.gun_library import AR_15
from entities.weapons.gun import Gun


game = Game()
hunter = Player("Hunter", "hunter", game)

game.switch_state(game.playing_state)

gun = Gun(AR_15)
hunter.attempt_pickup_weapon(gun)


print("\n-----------------------------")
print("Movement Test")
print("-----------------------------")

hunter.position = (100, 100)

hunter.attempt_add_effect(
    ApplyMovementModifierEffect(
        SpeedMultiplier(2.0)
    )
)

hunter.attempt_move((101, 100))

print("Expected: (102, 100)")
print("Actual:  ", hunter.position)


print("\n-----------------------------")
print("Damage Test")
print("-----------------------------")

hunter.attempt_add_effect(
    ApplyShotValueModifierEffect(
        DamageMultiplier(2.0)
    )
)

hunter.attempt_use_weapon()