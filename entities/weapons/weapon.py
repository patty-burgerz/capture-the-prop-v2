from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.player import Player


class Weapon:
    """
    Base class for all weapons (guns, gadgets, cursed items, etc.).

    Important design notes:
    - Weapons do NOT decide whether they are allowed to be used.
      That decision is handled by the Game + current match State.
    - Weapons do NOT know about match phases (lobby / preparing / playing).
    - Weapons do NOT mutate the world directly.

    A weapon's job is simple:
    - Read its own state (owner, ammo, spec, etc.)
    - Attempt to produce a ShotIntent (or equivalent)
    - Return None if it cannot be used
    """

    def __init__(self, name: str):
        self.name = name

        # The owning player is assigned by the Game when the weapon is picked up.
        # Weapons do not assign or change ownership themselves.
        self.owner: Optional["Player"] = None

    def use(self):
        """
        Attempt to use the weapon.

        Returns:
            - A ShotIntent-like object if the weapon can be used
            - None if the weapon cannot be used (no owner, no ammo, etc.)

        Subclasses MUST override this method.
        """
        raise NotImplementedError