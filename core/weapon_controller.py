from __future__ import annotations

from typing import TYPE_CHECKING

from entities.weapons.shot_intent import ShotIntent
from entities.Bullet import Bullet

if TYPE_CHECKING:
    from core.game import Game
    from entities.player import Player
    from entities.weapons.weapon import Weapon


class WeaponController:
    def __init__(self, game: "Game"):
        self.game = game

    def switch_slot(self, player, slot_name: str):
        if slot_name not in player.loadout:
            self.game.notify_player(player, f"Invalid slot: {slot_name}")
            return None
        player.current_weapon_slot = slot_name
        self.game.notify_player(player, f"Switched to {slot_name}")
        return True

    def pickup_into_slot(self, player, weapon: "Weapon", slot_name: str):
        if weapon.owner is not None:
            self.game.notify_player(player, f"{weapon.name} is already owned.")
            return None

        old = player.loadout.get(slot_name)
        if old:
            old.owner = None
            self.game.notify_all(f"{player.name} dropped {old.name}.")

        weapon.owner = player
        player.loadout[slot_name] = weapon
        self.game.notify_all(f"{player.name} picked up {weapon.name} into {slot_name}.")
        return True

    def get_use_result_or_none(self, player):
        weapon = player.loadout.get(player.current_weapon_slot)
        if not weapon:
            self.game.notify_player(player, "No weapon equipped in current slot.")
            return None, None

        use_result = weapon.use()
        if use_result is None:
            self.game.notify_player(player, f"Cannot use {weapon.name} right now.")
            return weapon, None

        return weapon, use_result

    def use_equipped_live(self, player):
        weapon, use_result = self.get_use_result_or_none(player)
        if use_result is None:
            return None

        if isinstance(use_result, ShotIntent):
            final_shot = player.active_effects.modify_shot(use_result)
            return self.execute_shot_intent(player, final_shot)

        self.game.notify_player(player, f"{weapon.name} use is not implemented yet.")
        return None

    def use_equipped_blank(self, player):
        weapon, use_result = self.get_use_result_or_none(player)
        if use_result is None:
            return None

        if isinstance(use_result, ShotIntent):
            self.game.notify_player(player, f"{player.name} fired a blank!")
            return True

        self.game.notify_player(player, f"{weapon.name} use is not implemented yet.")
        return None

    def execute_shot_intent(self, player, shot_intent: ShotIntent):
        x, y = player.position
        dx, dy = player.direction

        speed = float(shot_intent.bullet_speed)
        vx = dx * speed
        vy = dy * speed

        bullet = Bullet(
            x=float(x),
            y=float(y),
            vx=float(vx),
            vy=float(vy),
            owner_id=player.name,
            damage=int(shot_intent.damage),
            ttl=2.0,
            travel=shot_intent.travel_behavior,
            impact=shot_intent.impact_behavior
        )
        self.game.bullets.append(bullet)
        self.game.notify_player(player, f"Fired {shot_intent.spec.name}")
        return True
