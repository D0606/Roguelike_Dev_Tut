#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handler import EventHandler


def main() -> None:
    screen_width = 80
    screen_height = 50
    # Need to be cast to int or else uses float
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="My roguelike dev experiment.",
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        # Game play loop
        while True:
            # Print the string to the co-ordinates
            root_console.print(x=player_x, y=player_y, string="@")

            # Update the display
            context.present(root_console)

            # Clear previous prints
            root_console.clear()

            # Wait for a user input event and close gracefully if quit is used (top-right X)
            for event in tcod.event.wait():

                # Action is sent to the EventHandler event and the appropriate action assigned
                action = event_handler.dispatch(event)

                # Do nothing
                if action is None:
                    continue

                # Process movement by value assigned
                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                # Close game gracefully
                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()
