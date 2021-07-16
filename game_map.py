from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entities import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")    # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")   # Tiles the player has explored before

    def check_blocking_entity_location(self, location_x: int, location_y: int,) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        # Return true if x and y are inside bounds of map
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        # Visible tiles drawn in "light"
        # Explored but not visible in "dark"
        # Unexplored tiles in "SHROUD" - default
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities in player LOS
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, entity.colour)
