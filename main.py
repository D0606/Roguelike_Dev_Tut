#!/usr/bin/env python3
import tcod


def main() -> None:
    screen_width = 80
    screen_height = 50
    player_X = (screen_width/2)
    player_Y = (screen_height/2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="My roguelike dev experiment.",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        #Gameplay loop
        while True:
            #Print the string to the co-ordinates
            root_console.print(x=player_X, y=player_Y, string="@")

            #Update the display
            context.present(root_console)

            #Wait for a user input event and close gracefully if quit is used (top-right X)
            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()

if __name__ == "__main__":
    main()