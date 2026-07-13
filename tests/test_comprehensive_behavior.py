"""
Comprehensive behavioral tests covering all game engine mechanics.

Tests organized by coverage area:
- State Policy (Lobby, Preparing, Playing rules)
- Action Coverage (all actions in all states)
- Weapon Pipeline (pickup, switch, fire, ammo)
- Effect Pipeline (slot independence, replacement, modification)
- World Simulation (bullet movement, TTL, cleanup)
- Controller Delegation (Game facade)
- Integration (complete gameplay flow)
"""

import unittest
from core.game import Game
from entities.player import Player
from entities.weapons.gun import Gun
from entities.weapons.gun_library import AR_15, GLOCK_17
from entities.effects import DoubleDamageEffect, SpeedBoostEffect
from entities.Bullet import Bullet


# ============================================================
# STATE POLICY COVERAGE
# ============================================================

class TestLobbyPolicy(unittest.TestCase):
    """Verify Lobby state policy."""

    def setUp(self):
        self.game = Game()
        self.player = Player("LobbyTest", "hunter", self.game)
        self.game.switch_state(self.game.lobby_state)

    def test_lobby_allows_move(self):
        """Lobby allows move."""
        self.player.position = (0, 0)
        result = self.player.attempt_move((10, 20))
        self.assertTrue(result)

    def test_lobby_denies_pickup_weapon(self):
        """Lobby denies weapon pickup."""
        weapon = Gun(AR_15, starting_ammo=10)
        result = self.player.attempt_pickup_weapon(weapon)
        self.assertFalse(result)

    def test_lobby_denies_use_weapon(self):
        """Lobby denies weapon use."""
        self.player.loadout["primary"] = Gun(AR_15, starting_ammo=10)
        result = self.player.attempt_use_weapon()
        self.assertFalse(result)

    def test_lobby_denies_set_shot_effect(self):
        """Lobby denies shot effect assignment."""
        result = self.player.attempt_set_shot_effect(DoubleDamageEffect())
        self.assertFalse(result)

    def test_lobby_denies_set_movement_effect(self):
        """Lobby denies movement effect assignment."""
        result = self.player.attempt_set_movement_effect(SpeedBoostEffect())
        self.assertFalse(result)


class TestPreparingPolicy(unittest.TestCase):
    """Verify Preparing state policy."""

    def setUp(self):
        self.game = Game()
        self.player = Player("PrepTest", "hunter", self.game)
        self.game.switch_state(self.game.preparing_state)

    def test_preparing_allows_pickup(self):
        """Preparing allows weapon pickup."""
        weapon = Gun(AR_15, starting_ammo=10)
        result = self.player.attempt_pickup_weapon(weapon)
        self.assertTrue(result)

    def test_preparing_allows_move(self):
        """Preparing allows move."""
        self.player.position = (0, 0)
        result = self.player.attempt_move((10, 20))
        self.assertTrue(result)

    def test_preparing_blank_fire_no_bullets(self):
        """Preparing blank fire doesn't create bullets."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        initial = len(self.game.bullets)
        self.player.attempt_use_weapon()
        self.assertEqual(len(self.game.bullets), initial)

    def test_preparing_consumes_ammo(self):
        """Preparing fire consumes ammo."""
        weapon = Gun(AR_15, starting_ammo=5)
        self.player.loadout["primary"] = weapon
        self.player.attempt_use_weapon()
        self.assertEqual(weapon.ammo, 4)

    def test_preparing_denies_set_shot_effect(self):
        """Preparing denies shot effect."""
        result = self.player.attempt_set_shot_effect(DoubleDamageEffect())
        self.assertFalse(result)


class TestPlayingPolicy(unittest.TestCase):
    """Verify Playing state policy."""

    def setUp(self):
        self.game = Game()
        self.player = Player("PlayingTest", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def test_playing_allows_pickup(self):
        """Playing allows weapon pickup."""
        weapon = Gun(AR_15, starting_ammo=10)
        result = self.player.attempt_pickup_weapon(weapon)
        self.assertTrue(result)

    def test_playing_live_fire_creates_bullets(self):
        """Playing live fire creates bullets."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        initial = len(self.game.bullets)
        self.player.attempt_use_weapon()
        self.assertGreater(len(self.game.bullets), initial)

    def test_playing_allows_set_shot_effect(self):
        """Playing allows shot effect."""
        result = self.player.attempt_set_shot_effect(DoubleDamageEffect())
        self.assertIsNone(result)  # Returns None on success

    def test_playing_allows_set_movement_effect(self):
        """Playing allows movement effect."""
        result = self.player.attempt_set_movement_effect(SpeedBoostEffect())
        self.assertIsNone(result)


# ============================================================
# WEAPON PIPELINE COVERAGE
# ============================================================

class TestWeaponPickup(unittest.TestCase):
    """Test weapon pickup mechanics."""

    def setUp(self):
        self.game = Game()
        self.player = Player("WeaponTest", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def test_pickup_assigns_weapon(self):
        """Pickup assigns weapon to slot."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        self.assertIs(self.player.loadout["primary"], weapon)

    def test_pickup_sets_owner(self):
        """Pickup sets weapon owner."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        self.assertIs(weapon.owner, self.player)

    def test_pickup_replaces_existing(self):
        """Pickup replaces existing weapon in slot."""
        w1 = Gun(AR_15, starting_ammo=10)
        w2 = Gun(GLOCK_17, starting_ammo=10)
        self.player.attempt_pickup_weapon(w1)
        self.player.attempt_pickup_weapon(w2)
        self.assertIs(self.player.loadout["primary"], w2)
        self.assertIsNone(w1.owner)


class TestWeaponSwitch(unittest.TestCase):
    """Test weapon slot switching."""

    def setUp(self):
        self.game = Game()
        self.player = Player("SwitchTest", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def test_switch_to_occupied_slot(self):
        """Can switch to occupied slot."""
        w1 = Gun(AR_15, starting_ammo=10)
        w2 = Gun(GLOCK_17, starting_ammo=10)
        self.player.attempt_pickup_weapon(w1)
        self.player.loadout["secondary"] = w2
        result = self.player.attempt_switch_slot("secondary")
        self.assertTrue(result)
        self.assertEqual(self.player.current_weapon_slot, "secondary")

    def test_switch_to_empty_slot_fails(self):
        """Cannot switch to empty slot."""
        w1 = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(w1)
        result = self.player.attempt_switch_slot("secondary")
        self.assertIsNone(result)  # Returns None, not False


class TestAmmoConsumption(unittest.TestCase):
    """Test ammo consumption."""

    def setUp(self):
        self.game = Game()
        self.player = Player("AmmoTest", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def test_fire_consumes_ammo(self):
        """Fire consumes one ammo."""
        weapon = Gun(AR_15, starting_ammo=5)
        self.player.attempt_pickup_weapon(weapon)
        self.player.attempt_use_weapon()
        self.assertEqual(weapon.ammo, 4)

    def test_fire_with_zero_ammo_fails(self):
        """Fire with zero ammo fails."""
        weapon = Gun(AR_15, starting_ammo=1)
        self.player.attempt_pickup_weapon(weapon)
        self.player.attempt_use_weapon()
        result = self.player.attempt_use_weapon()
        self.assertFalse(result)


# ============================================================
# EFFECT PIPELINE COVERAGE
# ============================================================

class TestEffectAssignment(unittest.TestCase):
    """Test effect assignment and modification."""

    def setUp(self):
        self.game = Game()
        self.player = Player("EffectTest", "hunter", self.game)
        self.game.switch_state(self.game.playing_state)

    def test_shot_effect_modifies_damage(self):
        """Shot effect modifies bullet damage."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        self.player.attempt_use_weapon()
        self.assertEqual(self.game.bullets[0].damage, AR_15.damage * 2)

    def test_movement_effect_multiplies_position(self):
        """Movement effect multiplies movement."""
        self.player.position = (0, 0)
        self.player.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))
        self.player.attempt_move((10, 20))
        self.assertEqual(self.player.position, (20, 40))

    def test_effects_independent(self):
        """Shot and movement effects don't interfere."""
        weapon = Gun(AR_15, starting_ammo=10)
        self.player.attempt_pickup_weapon(weapon)
        self.player.position = (0, 0)
        self.player.active_effects.set_shot_effect(DoubleDamageEffect())
        self.player.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))
        self.player.attempt_use_weapon()
        self.player.attempt_move((10, 20))
        self.assertEqual(self.game.bullets[0].damage, AR_15.damage * 2)
        self.assertEqual(self.player.position, (20, 40))


# ============================================================
# WORLD SIMULATION COVERAGE
# ============================================================

class TestBulletSimulation(unittest.TestCase):
    """Test bullet movement and TTL."""

    def setUp(self):
        self.game = Game()

    def test_bullet_ttl_decreases(self):
        """Bullet TTL decreases on update."""
        bullet = Bullet(0, 0, 1, 0, "test", 10, 1.0, 5.0)
        self.game.bullets.append(bullet)
        self.game.update(1.0)
        self.assertEqual(bullet.ttl, 4.0)

    def test_dead_bullet_removed(self):
        """Dead bullets removed on update."""
        dead = Bullet(0, 0, 1, 0, "test", 10, 1.0, 0.0)
        live = Bullet(0, 0, 1, 0, "test", 10, 1.0, 5.0)
        self.game.bullets = [dead, live]
        self.game.update(0.1)
        self.assertEqual(len(self.game.bullets), 1)
        self.assertIs(self.game.bullets[0], live)

    def test_bullet_moves(self):
        """Bullet moves each update."""
        bullet = Bullet(0, 0, 10, 0, "test", 10, 1.0, 5.0)
        self.game.bullets.append(bullet)
        self.game.update(1.0)
        self.assertGreater(bullet.x, 0)


# ============================================================
# CONTROLLER DELEGATION COVERAGE
# ============================================================

class TestGameFacade(unittest.TestCase):
    """Test Game delegates correctly to controllers."""

    def test_game_has_action_router(self):
        """Game has ActionRouter."""
        game = Game()
        self.assertIsNotNone(game.actions)

    def test_game_has_weapon_controller(self):
        """Game has WeaponController."""
        game = Game()
        self.assertIsNotNone(game.weapons)

    def test_game_has_effect_controller(self):
        """Game has EffectController."""
        game = Game()
        self.assertIsNotNone(game.effects)

    def test_game_has_world_controller(self):
        """Game has WorldController."""
        game = Game()
        self.assertIsNotNone(game.world)


# ============================================================
# INTEGRATION / SMOKE TEST
# ============================================================

class TestCompleteGameplayFlow(unittest.TestCase):
    """End-to-end gameplay scenario."""

    def test_full_hunt_scenario(self):
        """Complete hunt: setup, blank fire, live fire, effects, cleanup."""
        game = Game()
        hunter = Player("Hunter", "hunter", game)
        
        # Preparing phase
        game.switch_state(game.preparing_state)
        rifle = Gun(AR_15, starting_ammo=10)
        hunter.attempt_pickup_weapon(rifle)
        hunter.attempt_use_weapon()
        self.assertEqual(len(game.bullets), 0)
        
        # Playing phase
        game.switch_state(game.playing_state)
        hunter.active_effects.set_shot_effect(DoubleDamageEffect())
        hunter.attempt_use_weapon()
        self.assertEqual(len(game.bullets), 1)
        self.assertEqual(game.bullets[0].damage, AR_15.damage * 2)
        
        # Move with effects
        hunter.position = (0, 0)
        hunter.active_effects.set_movement_effect(SpeedBoostEffect(speed_multiplier=2.0))
        hunter.attempt_move((10, 20))
        self.assertEqual(hunter.position, (20, 40))
        
        # World update
        game.update(3.0)
        self.assertEqual(len(game.bullets), 0)  # Bullets expired


if __name__ == "__main__":
    unittest.main()

