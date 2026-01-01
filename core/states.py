from entities.player import Player
from entities.weapons.weapon import Weapon


class GameState:
    def __init__(self, game):
        self.game = game

    def handle_move(self, player: Player, new_position):
        raise NotImplementedError

    def handle_pickup_weapon(self, player: Player, weapon: Weapon):
        raise NotImplementedError

    def handle_switch_slot(self, player: Player, slot_name: str):
        raise NotImplementedError

    def handle_use_weapon(self, player: Player):
        raise NotImplementedError

    def handle_possess(self, player: Player, obj_name: str):
        raise NotImplementedError


class LobbyState(GameState):
    def handle_move(self, player, new_position):
        return self.game._move_core(player, new_position)

    def handle_pickup_weapon(self, player, weapon):
        self.game.notify_player(player, "Can't pick up weapons in the lobby.")
        return False

    def handle_switch_slot(self, player, slot_name):
        self.game.notify_player(player, "Can't switch weapons in the lobby.")
        return False

    def handle_use_weapon(self, player):
        self.game.notify_player(player, "Can't use weapons in the lobby.")
        return False

    def handle_possess(self, player, obj_name):
        self.game.notify_player(player, "Can't possess in the lobby.")
        return False


class PreparingState(GameState):
    def handle_move(self, player, new_position):
        return self.game._move_core(player, new_position)

    def handle_pickup_weapon(self, player, weapon):
        return self.game._pickup_weapon_into_slot_core(
            player, weapon, player.current_weapon_slot
        )

    def handle_switch_slot(self, player, slot_name):
        return self.game._switch_slot_core(player, slot_name)

    def handle_use_weapon(self, player):
        return self.game._use_equipped_weapon_blank_core(player)

    def handle_possess(self, player, obj_name):
        self.game.notify_all(f"{player.name} possessed {obj_name} (PREPARING)")
        return True


class PlayingState(GameState):
    def handle_move(self, player, new_position):
        return self.game._move_core(player, new_position)

    def handle_pickup_weapon(self, player, weapon):
        return self.game._pickup_weapon_into_slot_core(
            player, weapon, player.current_weapon_slot
        )

    def handle_switch_slot(self, player, slot_name):
        return self.game._switch_slot_core(player, slot_name)

    def handle_use_weapon(self, player):
        return self.game._use_equipped_weapon_live_core(player)

    def handle_possess(self, player, obj_name):
        self.game.notify_all(f"{player.name} possessed {obj_name} (PLAYING)")
        return True
