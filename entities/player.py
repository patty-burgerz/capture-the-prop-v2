from typing import Optional, Dict, TYPE_CHECKING

from core.status import Status
from entities.weapons.weapon import Weapon
from entities.effects import ActiveEffects

if TYPE_CHECKING:
    from core.game import Game


class Player:
    def __init__(self, name: str, role: str, game: "Game"):
        self.name = name
        self.role = role
        self.game = game

        self.position = (0, 0)
        self.direction = (1, 0)
        self.health = 100

        self.loadout: Dict[str, Optional[Weapon]] = {
            "primary": None,
            "secondary": None,
            "tertiary": None,
        }

        self.current_weapon_slot = "primary"
        self.status = Status()
        self.active_effects = ActiveEffects()

        if role == "hunter":
            self.game.add_hunter(self)
        elif role == "prop":
            self.game.add_prop(self)
        elif role == "guardian":
            self.game.add_guardian(self)


    # ---- ATTEMPTS (INTENT ONLY) ----

    def attempt_move(self, new_position):
        return self.game.attempt_move(self, new_position)

    def attempt_pickup_weapon(self, weapon: Weapon):
        return self.game.attempt_pickup_weapon(self, weapon)

    def attempt_switch_slot(self, slot_name: str):
        return self.game.attempt_switch_slot(self, slot_name)

    def attempt_use_weapon(self):
        return self.game.attempt_use_weapon(self)

    def attempt_possess(self, obj_name: str):
        return self.game.attempt_possess(self, obj_name)

    def attempt_set_shot_effect(self, effect):
        return self.game.attempt_set_shot_effect(self, effect)

    def attempt_set_movement_effect(self, effect):
        return self.game.attempt_set_movement_effect(self, effect)

    def update(self, message: str):
        print(f"[{self.role.upper()} {self.name}] {message}")

    # health
    def take_damage(self, amount: int):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.game._handle_player_death(self)
