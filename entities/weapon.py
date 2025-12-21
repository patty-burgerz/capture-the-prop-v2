from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player


class Weapon:
    def __init__(self, name: str):
        self.name = name
        self.owner: Optional["Player"] = None

    def use(self, context: Dict[str, Any]) -> None:
        owner_name = self.owner.name if self.owner else "Nobody"
        mode = context.get("mode", "real")
        print(f"[WEAPON] {self.name} used by {owner_name} (mode={mode}) but it does nothing.")

class Gun(Weapon):
    def use(self, context: Dict[str, Any]) -> None:
        owner_name = self.owner.name if self.owner else "Nobody"
        mode = context.get("mode", "real")
        if mode == "blank":
            print(f"[GUN] {owner_name} fires BLANKS with {self.name}. *click-bang*")
        else:
            print(f"[GUN] {owner_name} fires LIVE with {self.name}. *BANG*")
