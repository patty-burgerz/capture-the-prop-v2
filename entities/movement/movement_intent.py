from dataclasses import dataclass


Position = tuple[float, float]


@dataclass(frozen=True)
class MoveIntent:
    current_position: Position
    requested_position: Position