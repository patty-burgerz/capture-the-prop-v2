from typing import Optional, TYPE_CHECKING

from core.action_router import ActionRouter
from core.effect_controller import EffectController
from core.states import LobbyState, PreparingState, PlayingState
from core.weapon_controller import WeaponController
from core.world_controller import WorldController
from entities.player import Player
from entities.weapons.weapon import Weapon
from entities.weapons.shot_intent import ShotIntent
from entities.Bullet import Bullet

if TYPE_CHECKING:
    from entities.effects.active_effect import ActiveEffect


class Game:
    """
    Game is the authoritative orchestrator.
    - Routes player intent (attempt_* methods)
    - Delegates policy decisions to the current GameState
    - Executes irreversible world mutations in *_core methods

    For now, Game also acts as the World (ticks bullets).
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

        # World-simulated entities
        self.bullets: list[Bullet] = []

        self.actions = ActionRouter(self)
        self.effects = EffectController(self)
        self.weapons = WeaponController(self)
        self.world = WorldController(self)

    # ============================================================
    # Notifications (TEMPORARY / DEBUG-ORIENTED)
    # ============================================================

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

    def attempt_move(self, player: Player, new_position):
        return self.actions.attempt_move(player, new_position)

    def attempt_pickup_weapon(self, player: Player, weapon: Weapon):
        return self.actions.attempt_pickup_weapon(player, weapon)

    def attempt_switch_slot(self, player: Player, slot_name: str):
        return self.actions.attempt_switch_slot(player, slot_name)

    def attempt_use_weapon(self, player: Player):
        return self.actions.attempt_use_weapon(player)

    def attempt_possess(self, player: Player, obj_name: str):
        return self.actions.attempt_possess(player, obj_name)

    def attempt_set_shot_effect(self, player: Player, effect: "ActiveEffect"):
        return self.actions.attempt_set_shot_effect(player, effect)

    def attempt_set_movement_effect(self, player: Player, effect: "ActiveEffect"):
        return self.actions.attempt_set_movement_effect(player, effect)

    # ============================================================
    # CORE MECHANICS (WORLD MUTATION)
    # ============================================================
    
    def _move_core(self, player: Player, new_position):
        return self.actions.move_core(player, new_position)

    def _switch_slot_core(self, player: Player, slot_name: str):
        return self.weapons.switch_slot(player, slot_name)

    def _set_shot_effect_core(self, player: Player, effect) -> None:
        player.active_effects.set_shot_effect(effect)

    def _set_movement_effect_core(self, player: Player, effect) -> None:
        player.active_effects.set_movement_effect(effect)

    def _pickup_weapon_into_slot_core(self, player: Player, weapon: Weapon, slot_name: str):
        return self.weapons.pickup_into_slot(player, weapon, slot_name)

    # ============================================================
    # WORLD UPDATE (Game acts as World for now)
    # ============================================================

    def update(self, dt: float) -> None:
        self.world.update(dt)

    # ============================================================
    # WEAPON USE PIPELINE
    # ============================================================

    def _get_use_result_or_none(self, player: Player):
        return self.weapons.get_use_result_or_none(player)

    def _use_equipped_weapon_live_core(self, player: Player):
        return self.weapons.use_equipped_live(player)

    def _use_equipped_weapon_blank_core(self, player: Player):
        return self.weapons.use_equipped_blank(player)

    def _execute_shot_intent_core(self, player: Player, shot_intent: ShotIntent):
        return self.weapons.execute_shot_intent(player, shot_intent)

    def _set_shot_effect_core(self, player: Player, effect: "ActiveEffect"):
        return self.effects.set_shot_effect(player, effect)

    def _set_movement_effect_core(self, player: Player, effect: "ActiveEffect"):
        return self.effects.set_movement_effect(player, effect)
