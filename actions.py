from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entities import Entity


class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        # Do this with objects needed to determine scope
        # engine is the scope the action is performed in
        # entity is the object doing the action
        # Override by action subclass
        raise NotImplementedError()


# Used to escape out of the game
class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


# Used for player movements
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy


    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked by tile

        entity.move(self.dx, self.dy)
