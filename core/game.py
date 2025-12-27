from typing import Optional

from core.states import LobbyState, PreparingState, PlayingState
from entities.player import Player
from entities.weapons.weapon import Weapon
from entities.weapons.shot_intent import ShotIntent
from entities.Bullet import Bullet
from entities.travel_behavior import StraightTravel


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

        old = player.loadout.get(slot_name)
        if old:
            old.owner = None
            self.notify_all(f"{player.name} dropped {old.name}.")

        weapon.owner = player
        player.loadout[slot_name] = weapon
        self.notify_all(f"{player.name} picked up {weapon.name} into {slot_name}.")
        return True

    # ============================================================
    # WORLD UPDATE (Game acts as World for now)
    # ============================================================

    def update(self, dt: float) -> None:
        for bullet in self.bullets:
            bullet.update(self, dt)

        # Remove dead bullets safely
        self.bullets = [b for b in self.bullets if b.alive]
        print(len(self.bullets))

    # ============================================================
    # WEAPON USE PIPELINE
    # ============================================================

    def _use_equipped_weapon_core(self, player: Player):
        """
        Ask equipped weapon to produce a use-result (intent),
        then execute it.
        """
        weapon = player.loadout.get(player.current_weapon_slot)
        if not weapon:
            self.notify_player(player, "No weapon equipped in current slot.")
            return None

        use_result = weapon.use()
        if use_result is None:
            self.notify_player(player, f"Cannot use {weapon.name} right now.")
            return None

        if isinstance(use_result, ShotIntent):
            return self._execute_shot_intent_core(player, use_result)

        self.notify_player(player, f"{weapon.name} use is not implemented yet.")
        return None

    def _execute_shot_intent_core(self, player: Player, shot_intent: ShotIntent):
        """
        v1 execution:
        - Spawn a straight-travel bullet
        - No collision or impact yet
        """
        # Spawn at player's position
        x, y = player.position
        dx, dy = player.direction

        speed = float(shot_intent.spec.bullet_speed)
        vx = dx * speed
        vy = dy * speed

        bullet = Bullet(
            x=float(x),
            y=float(y),
            vx=float(vx),
            vy=float(vy),
            owner_id=player.name,  # replace with player.id later
            damage=int(shot_intent.spec.damage),
            ttl=2.0,
            travel=StraightTravel(),
        )

        self.bullets.append(bullet)

        # Temporary debug output
        self.notify_player(player, f"Fired {shot_intent.spec.name}")

        return True
