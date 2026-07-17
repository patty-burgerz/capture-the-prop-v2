"""Integration tests for Game's controller-based action pipelines."""

import unittest

from core.game import Game
from entities.effects.apply_movement_modifier_effect import (
    ApplyMovementModifierEffect,
)
from entities.movement.modifiers.speed_multiplier import SpeedMultiplier
from entities.movement.movement_intent import MoveIntent
from entities.player import Player
from entities.weapons.gun import Gun
from entities.weapons.gun_library import AR_15


class TestGameControllerRefactor(unittest.TestCase):
    def make_movement_effect(self):
        return ApplyMovementModifierEffect(SpeedMultiplier(2.0))

    def test_lobby_denies_effect_assignment(self):
        game = Game()
        player = Player("LobbyPlayer", "hunter", game)
        game.switch_state(game.lobby_state)
        effect = self.make_movement_effect()

        result = player.attempt_add_effect(effect)

        self.assertFalse(result)
        move = MoveIntent((0, 0), (10, 20))
        self.assertIs(player.active_effects.modify_movement(move), move)

    def test_preparing_denies_effect_assignment(self):
        game = Game()
        player = Player("PrepPlayer", "hunter", game)
        game.switch_state(game.preparing_state)
        effect = self.make_movement_effect()

        result = player.attempt_add_effect(effect)

        self.assertFalse(result)
        move = MoveIntent((0, 0), (10, 20))
        self.assertIs(player.active_effects.modify_movement(move), move)

    def test_playing_allows_effect_assignment(self):
        game = Game()
        player = Player("PlayingPlayer", "hunter", game)
        game.switch_state(game.playing_state)
        effect = self.make_movement_effect()

        result = player.attempt_add_effect(effect)

        self.assertIs(result, effect)
        move = MoveIntent((0, 0), (10, 20))
        modified_move = player.active_effects.modify_movement(move)
        self.assertEqual(modified_move.requested_position, (20.0, 40.0))

    def test_ammo_is_consumed_once_per_valid_trigger_pull(self):
        game = Game()
        player = Player("AmmoPlayer", "hunter", game)
        game.switch_state(game.playing_state)
        weapon = Gun(AR_15, starting_ammo=1)

        player.attempt_pickup_weapon(weapon)

        self.assertTrue(player.attempt_use_weapon())
        self.assertEqual(weapon.ammo, 0)
        self.assertEqual(len(game.bullets), 1)

        self.assertIsNone(player.attempt_use_weapon())
        self.assertEqual(weapon.ammo, 0)
        self.assertEqual(len(game.bullets), 1)

    def test_shot_uses_player_position_and_direction(self):
        game = Game()
        player = Player("DirectionPlayer", "hunter", game)
        game.switch_state(game.playing_state)
        player.position = (10, 20)
        player.direction = (0, -1)
        player.attempt_pickup_weapon(Gun(AR_15, starting_ammo=1))

        player.attempt_use_weapon()

        bullet = game.bullets[0]
        self.assertEqual((bullet.x, bullet.y), (10.0, 20.0))
        self.assertEqual((bullet.vx, bullet.vy), (0.0, -AR_15.bullet_speed))

    def test_dead_bullets_are_removed_during_world_updates(self):
        game = Game()
        player = Player("WorldPlayer", "hunter", game)
        game.switch_state(game.playing_state)
        player.attempt_pickup_weapon(Gun(AR_15, starting_ammo=2))

        player.attempt_use_weapon()
        player.attempt_use_weapon()
        dead_bullet, live_bullet = game.bullets
        dead_bullet.ttl = 0.0
        live_bullet.ttl = 1.0

        game.update(0.1)

        self.assertEqual(len(game.bullets), 1)
        self.assertIs(game.bullets[0], live_bullet)


if __name__ == "__main__":
    unittest.main()