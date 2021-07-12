class Action:
    pass


# Used to escape out of the game
class EscapeAction(Action):
    pass


# Used for player movements
class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy
