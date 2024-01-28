from ursina import *
from enum import Enum, auto
from math import sin, cos

app = Ursina()

window.color = color.black
camera.orthographic = True
camera.fov = 6


class Turn(Enum):
    Crow = auto()
    Vulture = auto()


class State:
    def __init__(self) -> None:
        self.turn = Turn.Crow
        self.num_crows = 0
        self.num_vultures = 0
        self.MAX_CROWS = 7

        self.selected_crow = None
        self.vulture_point = None

    def next_turn(self) -> None:
        match self.turn:
            case Turn.Crow:
                if self.num_crows < self.MAX_CROWS:
                    self.num_crows += 1
                self.turn = Turn.Vulture
                if self.vulture_point is not None:
                    self.vulture_point.scale = 0.5
            case Turn.Vulture:
                self.vulture_point.scale = 0.3
                if self.num_vultures == 0:
                    self.num_vultures += 1
                self.turn = Turn.Crow


class PointState(Enum):
    Empty = auto()
    Crow = auto()
    Vulture = auto()


class Point(Sprite):
    instances = []

    def __init__(self, x, y) -> None:
        super().__init__(texture=None, model="circle", collider="sphere")
        self.to_empty()
        self.x = x
        self.y = y
        Point.instances.append(self)

    def to_empty(self) -> None:
        self.point_state = PointState.Empty
        self.color = color.white
        self.scale = 0.3

    def to_crow(self) -> None:
        self.point_state = PointState.Crow
        self.color = color.green
        self.scale = 0.3

    def to_vulture(self) -> None:
        self.point_state = PointState.Vulture
        self.color = color.red
        state.vulture_point = self
        self.scale = 0.3

    def on_click(self) -> None:
        match state.turn:
            case Turn.Vulture:
                if state.num_vultures == 0:
                    if self.point_state == PointState.Empty:
                        self.to_vulture()
                        state.next_turn()
                else:
                    match self.point_state:
                        case PointState.Vulture:
                            # Ignore
                            pass
                        case PointState.Crow:
                            # Try to eat the crow
                            pass
                        case PointState.Empty:
                            # Try to move vulture here
                            state.vulture_point.to_empty()
                            self.to_vulture()
                            state.next_turn()
            case Turn.Crow:
                if state.num_crows == state.MAX_CROWS:
                    match self.point_state:
                        case PointState.Vulture:
                            # Ignore
                            pass
                        case PointState.Crow:
                            # Select this point
                            if state.selected_crow is not None:
                                state.selected_crow.scale = 0.3
                            state.selected_crow = self
                            state.selected_crow.scale = 0.5
                        case PointState.Empty:
                            # Try to move selected point here
                            if state.selected_crow is not None:
                                state.selected_crow.to_empty()
                                state.selected_crow = None
                                self.to_crow()
                                state.next_turn()
                else:
                    if self.point_state == PointState.Empty:
                        self.to_crow()
                        state.next_turn()


if __name__ == "__main__":
    state = State()
    d = sin(126 * pi / 180) / sin(18 * pi / 180)
    inner_points = [Point(sin(2 * pi * i / 5), cos(2 * pi * i / 5)) for i in range(5)]
    outer_points = [
        Point(d * sin(2 * pi * i / 5 + pi / 5), d * cos(2 * pi * i / 5 + pi / 5))
        for i in range(5)
    ]
    lines = [
        Sprite(
            model="line",
            position=(
                (outer_points[i].x + outer_points[(i + 2) % 5].x) / 2,
                (outer_points[i].y + outer_points[(i + 2) % 5].y) / 2,
                1,
            ),
            rotation=(0, 0, 72 * (i - 1)),
            scale=distance_2d(outer_points[0], outer_points[2]),
        )
        for i in range(5)
    ]
    app.run()
