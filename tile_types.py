from typing import Tuple

import numpy as np # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),   # Unicode codepoint
        ("fg", "3B"),       # 3 unsigned bytes for RGB colour
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data
tile_dt = np.dtype(
    [
        ("walkable", np.bool),      # True if tile can be walked upon
        ("transparent", np.bool),   # True is tile does not block LOS
        ("dark", graphic_dt),       # Graphics for when tile is not in LOS
        ("light", graphic_dt),      # Graphics for a tile in LOS
    ]
)


def new_tile(
        *,  # Enforce use of keywords so that parameter order doesn't matter
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    # Helper function for defining individual tile types
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD is used for unexplored tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50)),
)