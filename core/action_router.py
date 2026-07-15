from __future__ import annotations

from typing import TYPE_CHECKING

from entities.player import Player
from entities.weapons.weapon import Weapon

if TYPE_CHECKING:
    from core.game import Game


class ActionRouter:
    def __init__(self, game: "Game"):
        self.game = game

    def attempt_move(self, player: Player, new_position):
        if player.status.blocks("move"):
            self.game.notify_player(player, "Denied: you can't move right now.")
            return None
        return self.game.state.handle_move(player, new_position)

    def attempt_pickup_weapon(self, player: Player, weapon: Weapon):
        if player.status.blocks("pickup_weapon"):
            self.game.notify_player(player, "Denied: you can't pick up weapons right now.")
            return None
        return self.game.state.handle_pickup_weapon(player, weapon)

    def attempt_switch_slot(self, player: Player, slot_name: str):
        if player.status.blocks("switch_slot"):
            self.game.notify_player(player, "Denied: you can't switch weapons right now.")
            return None
        return self.game.state.handle_switch_slot(player, slot_name)

    def attempt_use_weapon(self, player: Player):
        if player.status.blocks("use_weapon"):
            self.game.notify_player(player, "Denied: you can't use weapons right now.")
            return None
        return self.game.state.handle_use_weapon(player)

    def attempt_possess(self, player: Player, obj_name: str):
        return self.game.state.handle_possess(player, obj_name)

    def attempt_set_shot_effect(self, player: Player, effect):
        return self.game.state.handle_set_shot_effect(player, effect)

    def attempt_set_movement_effect(self, player: Player, effect):
        return self.game.state.handle_set_movement_effect(player, effect)
