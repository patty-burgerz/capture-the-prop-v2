from typing import Optional

from core.states import LobbyState, PreparingState, PlayingState
from entities.player import Player
from entities.weapons.weapon import Weapon
from entities.weapons.shot_intent import ShotIntent


class Game:
    """
    Game is the authoritative orchestrator.
    - Routes player intent (attempt_* methods)
    - Delegates policy decisions to the current GameState
    - Executes irreversible world mutations in *_core methods
    """

    def __init__(self):
        # Teams
        self.hunters: list[Player] = []
        self.props: list[Player] = []
        self.guardian_angels: list[Player] = []

        # Match phase states (policy layer)
        self.lobby_state = LobbyState(self)
        self.preparing_state = PreparingState(self)
        self.playing_state = PlayingState(self)

        # Default state for now
        self.state = self.preparing_state

    # ============================================================
    # Notifications (TEMPORARY / DEBUG-ORIENTED)
    # ============================================================
    # These will likely evolve into event systems, audio cues,
    # visibility-filtered messaging, etc.

    def notify_all(self, message: str, exclude: Optional[Player] = None):
        for p in self.hunters + self.props + self.guardian_angels:
            if p is not exclude:
                p.update(message)

    def notify_player(self, player: Player, message: str):
        player.update(message)

    # ============================================================
    # Registration
    # ============================================================

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
        """
        Switch the active match phase.
        States control *policy*, not mechanics.
        """
        self.state = new_state
        self.notify_all(f"Game state switched to {type(new_state).__name__}")

    # ============================================================
    # ATTEMPT ROUTERS (PLAYER INTENT)
    # ============================================================
    # Player objects never mutate the world directly.
    # They express intent; Game + State decide what happens.

    def attempt_move(self, player: Player, new_position):
        return self.state.handle_move(player, new_position)

    def attempt_pickup_weapon(self, player: Player, weapon: Weapon):
        if player.status.blocks("pickup_weapon"):
            self.notify_player(player, "Denied: you can't pick up weapons right now.")
            return None
        return self.state.handle_pickup_weapon(player, weapon)

    def attempt_switch_slot(self, player: Player, slot_name: str):
        if player.status.blocks("switch_slot"):
            self.notify_player(player, "Denied: you can't switch weapons right now.")
            return None
        return self.state.handle_switch_slot(player, slot_name)

    def attempt_use_weapon(self, player: Player):
        if player.status.blocks("use_weapon"):
            self.notify_player(player, "Denied: you can't use weapons right now.")
            return None
        return self.state.handle_use_weapon(player)

    def attempt_possess(self, player: Player, obj_name: str):
        return self.state.handle_possess(player, obj_name)

    # ============================================================
    # CORE MECHANICS (WORLD MUTATION)
    # ============================================================
    # These methods are called ONLY after authorization.
    # No state checks, no player input here.

    def _move_core(self, player: Player, new_position):
        player.position = new_position
        return True

    def _switch_slot_core(self, player: Player, slot_name: str):
        if slot_name not in player.loadout:
            self.notify_player(player, f"Invalid slot: {slot_name}")
            return None
        player.current_weapon_slot = slot_name
        self.notify_player(player, f"Switched to {slot_name}")
        return True

    def _pickup_weapon_into_slot_core(self, player: Player, weapon: Weapon, slot_name: str):
        if weapon.owner is not None:
            self.notify_player(player, f"{weapon.name} is already owned.")
            return None

        # Drop old weapon in this slot, if any
        old = player.loadout.get(slot_name)
        if old:
            old.owner = None
            self.notify_all(f"{player.name} dropped {old.name}.")

        weapon.owner = player
        player.loadout[slot_name] = weapon
        self.notify_all(f"{player.name} picked up {weapon.name} into {slot_name}.")
        return True

    # ============================================================
    # WEAPON USE PIPELINE
    # ============================================================
    # This is the heart of the “intent → execution” architecture.

    def _use_equipped_weapon_core(self, player: Player):
        """
        Generic weapon use entry point.
        - Asks the equipped weapon to produce a use-result (intent).
        - Dispatches execution based on the type of result.
        """

        weapon = player.loadout.get(player.current_weapon_slot)
        if not weapon:
            self.notify_player(player, "No weapon equipped in current slot.")
            return None

        # Weapon decides whether it can act and what it produces.
        use_result = weapon.use()
        if use_result is None:
            self.notify_player(player, f"Cannot use {weapon.name} right now.")
            return None

        # Intent-based dispatch (Option 2 – explicit and readable)
        if isinstance(use_result, ShotIntent):
            return self._execute_shot_intent_core(player, use_result)

        # Future:
        # elif isinstance(use_result, MeleeIntent):
        #     return self._execute_melee_intent_core(player, use_result)

        self.notify_player(player, f"{weapon.name} use is not implemented yet.")
        return None

    def _execute_shot_intent_core(self, player: Player, shot_intent: ShotIntent):
        """
        Convert a ShotIntent into world effects.

        v1:
        - No bullets yet
        - No raycasts yet
        - Just confirms the shot occurred

        Future:
        - Create Bullet
        - Resolve travel + impact strategies
        - Add bullet to world simulation
        """
        self.notify_player(
            player,
            f"{player.name} fired {shot_intent.spec.name}!"
        )
        return True
