"""Tests for the current composed effect system."""

import unittest
from unittest.mock import MagicMock

from core.game import Game
from entities.effects.active_effects import ActiveEffects
from entities.effects.add_impact_effect import AddImpactEffect
from entities.effects.apply_movement_modifier_effect import (
    ApplyMovementModifierEffect,
)
from entities.effects.apply_shot_value_modifier_effect import (
    ApplyShotValueModifierEffect,
)
from entities.effects.replace_travel_effects import ReplaceTravelEffect
from entities.movement.modifiers.speed_multiplier import SpeedMultiplier
from entities.movement.movement_intent import MoveIntent
from entities.player import Player
from entities.weapons.gun import Gun
from entities.weapons.gun_library import AR_15
from entities.weapons.impact.damage_impact import DamageImpact
from entities.weapons.impact.yeet_impact import YeetImpact
from entities.weapons.shot_intent import ShotIntent
from entities.weapons.shot_values.damage_multiplier import DamageMultiplier
from entities.weapons.travel.straight_travel import StraightTravel
from entities.weapons.travel.travel_behavior import TravelBehavior


class TestTravel(TravelBehavior):
    """Simple alternate travel behavior used only by these tests."""

    def update(self, bullet, world, dt):
        pass


def make_shot_intent():
    """Return a fresh, predictable shot intent for unit tests."""
    return ShotIntent(
        name="Test gun",
        damage=20,
        bullet_speed=30.0,
        spread_deg=1.0,
        travel_behavior=StraightTravel(),
        impact_behaviors=(DamageImpact(),),
    )


class TestActiveEffectsUnit(unittest.TestCase):
    """Test effect composition without involving Game or Player."""

    def test_empty_effects_leave_shot_unchanged(self):
        effects = ActiveEffects()
        shot = make_shot_intent()

        result = effects.modify_shot(shot)

        self.assertIs(result, shot)

    def test_empty_effects_leave_movement_unchanged(self):
        effects = ActiveEffects()
        move = MoveIntent(
            current_position=(0, 0),
            requested_position=(10, 20),
        )

        result = effects.modify_movement(move)

        self.assertIs(result, move)

    def test_damage_multiplier_changes_only_damage(self):
        effects = ActiveEffects()
        effects.add_effect(
            ApplyShotValueModifierEffect(DamageMultiplier(2.0))
        )
        shot = make_shot_intent()

        result = effects.modify_shot(shot)

        self.assertEqual(result.damage, 40)
        self.assertEqual(result.bullet_speed, shot.bullet_speed)
        self.assertEqual(result.spread_deg, shot.spread_deg)
        self.assertIs(result.travel_behavior, shot.travel_behavior)
        self.assertEqual(result.impact_behaviors, shot.impact_behaviors)

    def test_latest_modifier_of_same_type_replaces_previous_one(self):
        effects = ActiveEffects()
        effects.add_effect(
            ApplyShotValueModifierEffect(DamageMultiplier(2.0))
        )
        effects.add_effect(
            ApplyShotValueModifierEffect(DamageMultiplier(3.0))
        )

        result = effects.modify_shot(make_shot_intent())

        self.assertEqual(result.damage, 60)

    def test_speed_multiplier_changes_requested_position(self):
        effects = ActiveEffects()
        effects.add_effect(
            ApplyMovementModifierEffect(SpeedMultiplier(2.0))
        )
        move = MoveIntent(
            current_position=(100, 100),
            requested_position=(101, 100),
        )

        result = effects.modify_movement(move)

        self.assertEqual(result.current_position, (100, 100))
        self.assertEqual(result.requested_position, (102.0, 100.0))

    def test_impact_effect_appends_instead_of_replacing(self):
        effects = ActiveEffects()
        effects.add_effect(AddImpactEffect(YeetImpact()))

        result = effects.modify_shot(make_shot_intent())

        self.assertEqual(len(result.impact_behaviors), 2)
        self.assertIsInstance(result.impact_behaviors[0], DamageImpact)
        self.assertIsInstance(result.impact_behaviors[1], YeetImpact)

    def test_travel_effect_replaces_travel_behavior(self):
        effects = ActiveEffects()
        replacement = TestTravel()
        effects.add_effect(ReplaceTravelEffect(replacement))

        result = effects.modify_shot(make_shot_intent())

        self.assertIs(result.travel_behavior, replacement)

    def test_unsupported_object_is_rejected(self):
        effects = ActiveEffects()

        with self.assertRaises(TypeError):
            effects.add_effect(object())


class TestEffectIntegration(unittest.TestCase):
    """Test effects through the real Player -> Game pipelines."""

    def setUp(self):
        self.game = Game()
        self.hunter = Player("Hunter", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def equip_ar_15(self):
        self.hunter.attempt_pickup_weapon(Gun(AR_15))

    def test_damage_effect_changes_spawned_bullet(self):
        self.equip_ar_15()
        self.hunter.attempt_add_effect(
            ApplyShotValueModifierEffect(DamageMultiplier(2.0))
        )

        self.hunter.attempt_use_weapon()

        self.assertEqual(len(self.game.bullets), 1)
        self.assertEqual(self.game.bullets[0].damage, AR_15.damage * 2)

    def test_movement_effect_changes_committed_position(self):
        self.hunter.position = (100, 100)
        self.hunter.attempt_add_effect(
            ApplyMovementModifierEffect(SpeedMultiplier(2.0))
        )

        self.hunter.attempt_move((101, 100))

        self.assertEqual(self.hunter.position, (102.0, 100.0))

    def test_bullet_contains_and_executes_both_impacts(self):
        self.equip_ar_15()
        self.hunter.attempt_add_effect(AddImpactEffect(YeetImpact()))
        self.hunter.attempt_use_weapon()
        bullet = self.game.bullets[-1]

        target = Player("Target", "prop", self.game)
        target.update = MagicMock()

        bullet.impact(target)

        self.assertEqual(target.health, 100 - AR_15.damage)
        target.update.assert_called_once_with(
            f"BONK! Yeet strength: {AR_15.damage * 1.0}"
        )
        self.assertFalse(bullet.alive)

    def test_shot_and_movement_effects_work_independently(self):
        self.equip_ar_15()
        self.hunter.position = (0, 0)
        self.hunter.attempt_add_effect(
            ApplyShotValueModifierEffect(DamageMultiplier(2.0))
        )
        self.hunter.attempt_add_effect(
            ApplyMovementModifierEffect(SpeedMultiplier(2.0))
        )

        self.hunter.attempt_use_weapon()
        self.hunter.attempt_move((10, 20))

        self.assertEqual(self.game.bullets[0].damage, AR_15.damage * 2)
        self.assertEqual(self.hunter.position, (20.0, 40.0))


class TestEffectAssignmentPolicy(unittest.TestCase):
    """Test that game state decides whether effects may be assigned."""

    def setUp(self):
        self.game = Game()
        self.player = Player("Player", "hunter", self.game)
        self.effect = ApplyMovementModifierEffect(SpeedMultiplier(2.0))

    def test_playing_state_allows_effect_assignment(self):
        self.game.switch_state(self.game.playing_state)

        result = self.player.attempt_add_effect(self.effect)

        self.assertIs(result, self.effect)

    def test_lobby_state_denies_effect_assignment(self):
        self.game.switch_state(self.game.lobby_state)

        result = self.player.attempt_add_effect(self.effect)

        self.assertFalse(result)
        move = MoveIntent((0, 0), (10, 20))
        self.assertIs(self.player.active_effects.modify_movement(move), move)

    def test_preparing_state_denies_effect_assignment(self):
        self.game.switch_state(self.game.preparing_state)

        result = self.player.attempt_add_effect(self.effect)

        self.assertFalse(result)
        move = MoveIntent((0, 0), (10, 20))
        self.assertIs(self.player.active_effects.modify_movement(move), move)


if __name__ == "__main__":
    unittest.main()