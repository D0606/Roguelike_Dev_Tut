from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


# This class is a subclass of tcod's EventDespatch class
class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        # Will be used in case of no valid keypress
        action: Optional[Action] = None

        # Holds the information regarding which key was pressed, no modifiers such as 'shift' or 'alt', etc
        key = event.sym

        # Movement key presses (up, down, left, right arrows)
        if key == tcod.event.K_UP:
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        # Escape key press
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key pressed
        return action