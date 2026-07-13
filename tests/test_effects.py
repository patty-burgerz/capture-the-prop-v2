"""
Tests for the typed shot and movement effects system.

Tests verify:
1. With no shot effect, the original ShotIntent is unchanged.
2. With the double-damage shot effect, damage is doubled before Bullet creation.
3. Assigning a new shot effect replaces the previous shot effect.
4. With no movement effect, movement behaves exactly as before.
5. With a movement effect, _move_core applies the transformed movement data.
6. A shot effect does not affect movement.
7. A movement effect does not affect shots.
8. Existing tests still pass.
"""

import unittest
from unittest.mock import MagicMock, patch

from core.game import Game
from entities.player import Player
from entities.weapons.gun import Gun
from entities.weapons.gun_library import GLOCK_17, AR_15
from entities.weapons.shot_intent import ShotIntent
from entities.effects import (
    ActiveEffect,
    ActiveEffects,
    DoubleDamageEffect,
    SpeedBoostEffect,
)


class TestActiveEffects(unittest.TestCase):
    """Test the ActiveEffects container."""
    
    def test_empty_container_returns_original_shot_intent(self):
        """With no shot effect, modify_shot returns the original ShotIntent unchanged."""
        effects = ActiveEffects()
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.0,
        )
        
        result = effects.modify_shot(shot)
        self.assertIs(result, shot, "Should return the exact same object")
        self.assertEqual(result.damage, 20)
    
    def test_empty_container_returns_original_movement(self):
        """With no movement effect, modify_movement returns the original movement unchanged."""
        effects = ActiveEffects()
        movement = (10, 20)
        
        result = effects.modify_movement(movement)
        self.assertIs(result, movement, "Should return the exact same object")
        self.assertEqual(result, (10, 20))
    
    def test_set_and_get_shot_effect(self):
        """Can set and retrieve a shot effect."""
        effects = ActiveEffects()
        effect = DoubleDamageEffect()
        
        effects.set_shot_effect(effect)
        self.assertIs(effects.get_shot_effect(), effect)
    
    def test_set_and_get_movement_effect(self):
        """Can set and retrieve a movement effect."""
        effects = ActiveEffects()
        effect = SpeedBoostEffect()
        
        effects.set_movement_effect(effect)
        self.assertIs(effects.get_movement_effect(), effect)
    
    def test_replace_shot_effect(self):
        """Assigning a new shot effect replaces the previous one."""
        effects = ActiveEffects()
        effect1 = DoubleDamageEffect()
        effect2 = DoubleDamageEffect()
        
        effects.set_shot_effect(effect1)
        self.assertIs(effects.get_shot_effect(), effect1)
        
        effects.set_shot_effect(effect2)
        self.assertIs(effects.get_shot_effect(), effect2)
        self.assertIsNot(effects.get_shot_effect(), effect1)
    
    def test_clear_shot_effect(self):
        """Can clear the shot effect by setting to None."""
        effects = ActiveEffects()
        effect = DoubleDamageEffect()
        
        effects.set_shot_effect(effect)
        effects.set_shot_effect(None)
        self.assertIsNone(effects.get_shot_effect())
    
    def test_modify_shot_applies_effect(self):
        """modify_shot applies the active effect."""
        effects = ActiveEffects()
        effect = DoubleDamageEffect()
        effects.set_shot_effect(effect)
        
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.0,
        )
        
        result = effects.modify_shot(shot)
        self.assertEqual(result.damage, 40)
        self.assertEqual(result.bullet_speed, 100.0)
    
    def test_modify_movement_applies_effect(self):
        """modify_movement applies the active effect."""
        effects = ActiveEffects()
        effect = SpeedBoostEffect(speed_multiplier=2.0)
        effects.set_movement_effect(effect)
        
        movement = (10, 20)
        result = effects.modify_movement(movement)
        self.assertEqual(result, (20, 40))


class TestDoubleDamageEffect(unittest.TestCase):
    """Test the DoubleDamageEffect."""
    
    def test_double_damage_doubles_damage(self):
        """DoubleDamageEffect doubles the damage of a shot."""
        effect = DoubleDamageEffect()
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.0,
        )
        
        result = effect.modify_shot(shot)
        self.assertEqual(result.damage, 40)
    
    def test_double_damage_preserves_other_fields(self):
        """DoubleDamageEffect only modifies damage, not other fields."""
        effect = DoubleDamageEffect()
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.5,
        )
        
        result = effect.modify_shot(shot)
        self.assertEqual(result.bullet_speed, 100.0)
        self.assertEqual(result.spread_deg, 0.5)
        self.assertIs(result.spec, shot.spec)
    
    def test_double_damage_does_not_affect_movement(self):
        """DoubleDamageEffect does not affect movement."""
        effect = DoubleDamageEffect()
        movement = (10, 20)
        
        result = effect.modify_movement(movement)
        self.assertIs(result, movement)


class TestSpeedBoostEffect(unittest.TestCase):
    """Test the SpeedBoostEffect."""
    
    def test_speed_boost_multiplies_movement(self):
        """SpeedBoostEffect multiplies movement coordinates."""
        effect = SpeedBoostEffect(speed_multiplier=2.0)
        movement = (10, 20)
        
        result = effect.modify_movement(movement)
        self.assertEqual(result, (20, 40))
    
    def test_speed_boost_with_custom_multiplier(self):
        """SpeedBoostEffect uses custom multiplier."""
        effect = SpeedBoostEffect(speed_multiplier=1.5)
        movement = (10, 20)
        
        result = effect.modify_movement(movement)
        self.assertEqual(result, (15, 30))
    
    def test_speed_boost_does_not_affect_shots(self):
        """SpeedBoostEffect does not affect shots."""
        effect = SpeedBoostEffect()
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.0,
        )
        
        result = effect.modify_shot(shot)
        self.assertIs(result, shot)


class TestActiveEffectIntegration(unittest.TestCase):
    """Integration tests with Game and Player."""
    
    def setUp(self):
        """Set up a game and player for testing."""
        self.game = Game()
        self.player = Player("TestPlayer", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)
    
    def test_player_has_active_effects(self):
        """Player has an active_effects attribute."""
        self.assertIsNotNone(self.player.active_effects)
        self.assertIsInstance(self.player.active_effects, ActiveEffects)
    
    def test_no_shot_effect_original_bullet(self):
        """With no shot effect, bullet has original damage."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        
        # Fire without effect
        self.player.attempt_use_weapon()
        self.assertEqual(len(self.game.bullets), 1)
        self.assertEqual(self.game.bullets[0].damage, 25)  # AR_15 base damage
    
    def test_double_damage_effect_doubles_bullet_damage(self):
        """With double-damage shot effect, bullet damage is doubled."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        
        # Apply double damage effect
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        
        # Fire with effect
        self.player.attempt_use_weapon()
        self.assertEqual(len(self.game.bullets), 1)
        self.assertEqual(self.game.bullets[0].damage, 50)  # 25 * 2
    
    def test_replacing_shot_effect(self):
        """Replacing a shot effect replaces behavior."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        
        # Apply first effect
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        self.player.attempt_use_weapon()
        first_damage = self.game.bullets[0].damage
        
        # Replace with no effect
        self.game.bullets = []  # Clear bullets
        self.player.active_effects.set_shot_effect(None)
        self.player.attempt_use_weapon()
        second_damage = self.game.bullets[0].damage
        
        self.assertEqual(first_damage, 50)
        self.assertEqual(second_damage, 25)
    
    def test_no_movement_effect_original_position(self):
        """With no movement effect, movement works as before."""
        self.player.position = (0, 0)
        
        self.player.attempt_move((10, 20))
        self.assertEqual(self.player.position, (10, 20))
    
    def test_movement_effect_transforms_movement(self):
        """With movement effect, _move_core applies the transformed movement."""
        self.player.position = (0, 0)
        effect = SpeedBoostEffect(speed_multiplier=2.0)
        self.player.active_effects.set_movement_effect(effect)
        
        self.player.attempt_move((10, 20))
        # With speed boost, (10, 20) becomes (20, 40)
        self.assertEqual(self.player.position, (20, 40))
    
    def test_shot_effect_does_not_affect_movement(self):
        """Shot effect does not affect movement."""
        self.player.position = (0, 0)
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        
        self.player.attempt_move((10, 20))
        self.assertEqual(self.player.position, (10, 20))
    
    def test_movement_effect_does_not_affect_shots(self):
        """Movement effect does not affect shot damage."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        
        # Apply movement effect only
        self.player.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))
        
        # Fire a shot
        self.player.attempt_use_weapon()
        self.assertEqual(len(self.game.bullets), 1)
        self.assertEqual(self.game.bullets[0].damage, 25)  # Original damage
    
    def test_both_effects_work_independently(self):
        """Shot and movement effects work independently."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        self.player.position = (0, 0)
        
        # Apply both effects
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        self.player.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))
        
        # Fire and move
        self.player.attempt_use_weapon()
        self.player.attempt_move((10, 20))
        
        # Verify both applied
        self.assertEqual(self.game.bullets[0].damage, 50)  # Double damage
        self.assertEqual(self.player.position, (20, 40))  # Speed boost


class TestEffectAssignmentStatePolicy(unittest.TestCase):
    """Tests for authoritative effect assignment through game state policy."""

    def setUp(self):
        self.game = Game()
        self.player = Player("TestPlayer", "hunter", self.game)

    def test_playing_state_allows_setting_shot_effect(self):
        self.game.switch_state(self.game.playing_state)
        effect = DoubleDamageEffect()

        result = self.player.attempt_set_shot_effect(effect)

        self.assertIsNone(result)
        self.assertIs(self.player.active_effects.get_shot_effect(), effect)

    def test_playing_state_allows_setting_movement_effect(self):
        self.game.switch_state(self.game.playing_state)
        effect = SpeedBoostEffect(speed_multiplier=2.0)

        result = self.player.attempt_set_movement_effect(effect)

        self.assertIsNone(result)
        self.assertIs(self.player.active_effects.get_movement_effect(), effect)

    def test_lobby_state_denies_setting_shot_effect(self):
        self.game.switch_state(self.game.lobby_state)
        original = DoubleDamageEffect()
        self.player.active_effects.set_shot_effect(original)

        result = self.player.attempt_set_shot_effect(DoubleDamageEffect())

        self.assertFalse(result)
        self.assertIs(self.player.active_effects.get_shot_effect(), original)

    def test_lobby_state_denies_setting_movement_effect(self):
        self.game.switch_state(self.game.lobby_state)
        original = SpeedBoostEffect(speed_multiplier=2.0)
        self.player.active_effects.set_movement_effect(original)

        result = self.player.attempt_set_movement_effect(SpeedBoostEffect(speed_multiplier=1.5))

        self.assertFalse(result)
        self.assertIs(self.player.active_effects.get_movement_effect(), original)

    def test_preparing_state_denies_setting_shot_effect(self):
        self.game.switch_state(self.game.preparing_state)
        original = DoubleDamageEffect()
        self.player.active_effects.set_shot_effect(original)

        result = self.player.attempt_set_shot_effect(DoubleDamageEffect())

        self.assertFalse(result)
        self.assertIs(self.player.active_effects.get_shot_effect(), original)

    def test_preparing_state_denies_setting_movement_effect(self):
        self.game.switch_state(self.game.preparing_state)
        original = SpeedBoostEffect(speed_multiplier=2.0)
        self.player.active_effects.set_movement_effect(original)

        result = self.player.attempt_set_movement_effect(SpeedBoostEffect(speed_multiplier=1.5))

        self.assertFalse(result)
        self.assertIs(self.player.active_effects.get_movement_effect(), original)

    def test_denied_request_leaves_existing_effects_unchanged(self):
        self.game.switch_state(self.game.lobby_state)
        original_shot = DoubleDamageEffect()
        original_movement = SpeedBoostEffect(speed_multiplier=2.0)
        self.player.active_effects.set_shot_effect(original_shot)
        self.player.active_effects.set_movement_effect(original_movement)

        self.player.attempt_set_shot_effect(DoubleDamageEffect())
        self.player.attempt_set_movement_effect(SpeedBoostEffect(speed_multiplier=1.5))

        self.assertIs(self.player.active_effects.get_shot_effect(), original_shot)
        self.assertIs(self.player.active_effects.get_movement_effect(), original_movement)

    def test_playing_state_can_clear_shot_slot_with_none(self):
        self.game.switch_state(self.game.playing_state)
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())

        self.player.attempt_set_shot_effect(None)

        self.assertIsNone(self.player.active_effects.get_shot_effect())

    def test_playing_state_can_clear_movement_slot_with_none(self):
        self.game.switch_state(self.game.playing_state)
        self.player.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))

        self.player.attempt_set_movement_effect(None)

        self.assertIsNone(self.player.active_effects.get_movement_effect())

    def test_setting_shot_effect_does_not_alter_movement_slot(self):
        self.game.switch_state(self.game.playing_state)
        movement_effect = SpeedBoostEffect(speed_multiplier=2.0)
        self.player.active_effects.set_movement_effect(movement_effect)

        self.player.attempt_set_shot_effect(DoubleDamageEffect())

        self.assertIs(self.player.active_effects.get_movement_effect(), movement_effect)

    def test_setting_movement_effect_does_not_alter_shot_slot(self):
        self.game.switch_state(self.game.playing_state)
        shot_effect = DoubleDamageEffect()
        self.player.active_effects.set_shot_effect(shot_effect)

        self.player.attempt_set_movement_effect(SpeedBoostEffect(speed_multiplier=1.5))

        self.assertIs(self.player.active_effects.get_shot_effect(), shot_effect)

    def test_second_effect_in_same_category_replaces_first(self):
        self.game.switch_state(self.game.playing_state)
        first = DoubleDamageEffect()
        second = DoubleDamageEffect()
        self.player.active_effects.set_shot_effect(first)

        self.player.attempt_set_shot_effect(second)

        self.assertIs(self.player.active_effects.get_shot_effect(), second)
        self.assertIsNot(self.player.active_effects.get_shot_effect(), first)


class TestBaseActiveEffect(unittest.TestCase):
    """Test the base ActiveEffect class."""
    
    def test_base_effect_returns_original_shot(self):
        """Base ActiveEffect returns original ShotIntent."""
        effect = ActiveEffect()
        shot = ShotIntent(
            spec=GLOCK_17,
            damage=20,
            bullet_speed=100.0,
            spread_deg=0.0,
        )
        
        result = effect.modify_shot(shot)
        self.assertIs(result, shot)
    
    def test_base_effect_returns_original_movement(self):
        """Base ActiveEffect returns original movement."""
        effect = ActiveEffect()
        movement = (10, 20)
        
        result = effect.modify_movement(movement)
        self.assertIs(result, movement)


if __name__ == "__main__":
    unittest.main()
