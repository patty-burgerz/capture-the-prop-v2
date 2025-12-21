from dataclasses import dataclass

@dataclass
class Status:
    stunned: bool = False
    ragdolled: bool = False

    def blocks(self, action: str) -> bool:
        if self.ragdolled and action in {"switch_slot", "use_weapon", "pickup_weapon"}:
            return True
        if self.stunned and action in {"switch_slot", "use_weapon", "pickup_weapon"}:
            return True
        return False
