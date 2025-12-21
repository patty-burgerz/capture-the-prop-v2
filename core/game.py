from typing import Optional
from core.states import LobbyState, PreparingState, PlayingState
from entities.weapon import Weapon
from entities.player import Player


class Game:
    def __init__(self):
        self.hunters = []
        self.props = []
        self.guardian_angels = []

        self.lobby_state = LobbyState(self)
        self.preparing_state = PreparingState(self)
        self.playing_state = PlayingState(self)

        self.state = self.preparing_state

    # ---- Notifications ----

    def notify_all(self, message: str, exclude: Optional[Player] = None):
        for p in self.hunters + self.props + self.guardian_angels:
            if p is not exclude:
                p.update(message)

    def notify_player(self, player: Player, message: str):
        player.update(message)

    # ---- Registration ----

    def add_hunter(self, player: Player):
        self.hunters.append(player)
        self.notify_all(f"{player.name} has joined the Hunters!")

    def add_prop(self, player: Player):
        self.props.append(player)
        self.notify_all(f"{player.name} has joined the Props!")

    def add_guardian(self, player: Player):
        self.guardian_angels.append(player)
        self.notify_all(f"{player.name} has joined the Guardian Angels!")

    def switch_state(self, new_state):
        self.state = new_state
        self.notify_all(f"Game state switched to {type(new_state).__name__}")

    # ---- ATTEMPT ROUTERS ----

    def attempt_move(self, player, new_position):
        return self.state.handle_move(player, new_position)

    def attempt_pickup_weapon(self, player, weapon: Weapon):
        if player.status.blocks("pickup_weapon"):
            self.notify_player(player, "Denied: you can't pick up weapons right now.")
            return False
        return self.state.handle_pickup_weapon(player, weapon)

    def attempt_switch_slot(self, player, slot_name):
        if player.status.blocks("switch_slot"):
            self.notify_player(player, "Denied: you can't switch weapons right now.")
            return False
        return self.state.handle_switch_slot(player, slot_name)

    def attempt_use_weapon(self, player):
        if player.status.blocks("use_weapon"):
            self.notify_player(player, "Denied: you can't use weapons right now.")
            return False
        return self.state.handle_use_weapon(player)

    def attempt_possess(self, player, obj_name):
        return self.state.handle_possess(player, obj_name)

    # ---- CORE MECHANICS ----

    def _move_core(self, player, new_position):
        player.position = new_position
        return True

    def _switch_slot_core(self, player, slot_name):
        if slot_name not in player.loadout:
            self.notify_player(player, f"Invalid slot: {slot_name}")
            return False
        player.current_weapon_slot = slot_name
        self.notify_player(player, f"Switched to {slot_name}")
        return True

    def _pickup_weapon_into_slot_core(self, player, weapon, slot_name):
        if weapon.owner is not None:
            self.notify_player(player, f"{weapon.name} is already owned.")
            return False

        old = player.loadout.get(slot_name)
        if old:
            old.owner = None
            self.notify_all(f"{player.name} dropped {old.name}.")

        weapon.owner = player
        player.loadout[slot_name] = weapon
        self.notify_all(f"{player.name} picked up {weapon.name} into {slot_name}.")
        return True

    def _use_weapon_core(self, player, mode="real"):
        weapon = player.loadout.get(player.current_weapon_slot)
        if not weapon:
            self.notify_player(player, "No weapon in current slot.")
            return False

        weapon.use({
            "mode": mode,
            "player": player,
            "slot": player.current_weapon_slot
        })
        return True
