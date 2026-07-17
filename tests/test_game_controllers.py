import unittest

from core.game import Game
from entities.player import Player
from entities.weapons.gun_library import AR_15
from entities.weapons.gun import Gun
from entities.effects import DoubleDamageEffect, SpeedBoostEffect
from entities.bullet import Bullet


class TestGameControllerRefactor(unittest.TestCase):
    def test_lobby_denies_effect_assignment(self):
        game = Game()
        player = Player("LobbyPlayer", "hunter", game)

        self.assertFalse(player.attempt_set_shot_effect(DoubleDamageEffect()))
        self.assertFalse(player.attempt_set_movement_effect(SpeedBoostEffect()))
        self.assertIsNone(player.active_effects.get_shot_effect())
        self.assertIsNone(player.active_effects.get_movement_effect())

    def test_preparing_denies_effect_assignment(self):
        game = Game()
        player = Player("PrepPlayer", "hunter", game)
        game.switch_state(game.preparing_state)

        self.assertFalse(player.attempt_set_shot_effect(DoubleDamageEffect()))
        self.assertFalse(player.attempt_set_movement_effect(SpeedBoostEffect()))
        self.assertIsNone(player.active_effects.get_shot_effect())
        self.assertIsNone(player.active_effects.get_movement_effect())

    def test_playing_allows_effect_assignment_and_keeps_slots_independent(self):
        game = Game()
        player = Player("PlayingPlayer", "hunter", game)
        game.switch_state(game.playing_state)

        shot_effect = DoubleDamageEffect()
        movement_effect = SpeedBoostEffect(speed_multiplier=2.0)

        self.assertIsNone(player.attempt_set_shot_effect(shot_effect))
        self.assertIsNone(player.attempt_set_movement_effect(movement_effect))

        self.assertIs(player.active_effects.get_shot_effect(), shot_effect)
        self.assertIs(player.active_effects.get_movement_effect(), movement_effect)

    def test_ammo_is_consumed_once_per_valid_trigger_pull(self):
        game = Game()
        player = Player("AmmoPlayer", "hunter", game)
        game.switch_state(game.playing_state)
        weapon = Gun(AR_15, starting_ammo=1)

        player.attempt_pickup_weapon(weapon)
        self.assertTrue(player.attempt_use_weapon())
        self.assertEqual(weapon.ammo, 0)
        self.assertEqual(len(game.bullets), 1)

        self.assertFalse(player.attempt_use_weapon())
        self.assertEqual(weapon.ammo, 0)
        self.assertEqual(len(game.bullets), 1)

    def test_dead_bullets_are_removed_during_world_updates(self):
        game = Game()
        dead_bullet = Bullet(0, 0, 0, 0, owner_id="player", damage=1, ttl=0.0)
        live_bullet = Bullet(0, 0, 0, 0, owner_id="player", damage=1, ttl=1.0)
        game.bullets = [dead_bullet, live_bullet]

        game.update(0.1)

        self.assertEqual(len(game.bullets), 1)
        self.assertIs(game.bullets[0], live_bullet)


if __name__ == "__main__":
    unittest.main()
