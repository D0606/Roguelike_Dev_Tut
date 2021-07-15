from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from entities import Entity


class RectangleRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def centre(self) -> Tuple[int, int]:
        centre_x = int((self.x1 + self.x2) / 2)
        centre_y = int((self.y1 + self.y2) / 2)

        return centre_x, centre_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        # Return the inner area of room as a 2D array index
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)


    def intersect_check(self, other: RectangleRoom) -> bool:
        # Return true if this room overlaps another rectangular room
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def joining_corridor(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    # Return an L-shaped tunnel between to points
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move horizontal then vertical
        corner_x, corner_y = x2, y1
    else:
        # Vertical then horizontal
        corner_x, corner_y = x1, y2

    # Generate the co-ordinates from this tunnel
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity,
) -> GameMap:
    # New dungeon map
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangleRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # RectangleRoom class makes rectangles easier to work with
        new_room = RectangleRoom(x, y, room_width, room_height)

        # Run through the other rooms and check for intersections
        if any(new_room.intersect_check(other_room) for other_room in rooms):
            continue    # This room intersects another, so try next attempt
        # If there are no intersections then room valid

        # Dig out the rooms inner area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room where the player begins
            player.x, player.y = new_room.centre
        else:   # All rooms after the first
            # Join this and previous room with corridor
            for x, y in joining_corridor(rooms[-1].centre, new_room.centre):
                dungeon.tiles[x, y] = tile_types.floor

        # Append the room to the list
        rooms.append(new_room)

    return dungeon
