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


class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy
        target = engine.game_map.check_blocking_entity_location(dest_x, dest_y)
        if not target:
            return  # No entity to attack

        print(f"You bump the {target.name}, making it jiggle!")


class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # Destination out of bounds
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return # Destination blocked by tile
        if engine.game_map.check_blocking_entity_location(dest_x, dest_y):
            return  # Destination blocked by entity

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.check_blocking_entity_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)

        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)