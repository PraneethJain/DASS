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

    def next_turn(self) -> None:
        match self.turn:
            case Turn.Crow:
                if self.num_crows < self.MAX_CROWS:
                    self.num_crows += 1
                self.turn = Turn.Vulture
            case Turn.Vulture:
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
        super().__init__(texture=None, model="circle", collider="sphere", scale=0.3)
        self.to_empty()
        self.x = x
        self.y = y
        Point.instances.append(self)

    def to_empty(self) -> None:
        self.point_state = PointState.Empty
        self.color = color.white

    def to_crow(self) -> None:
        self.point_state = PointState.Crow
        self.color = color.green

    def to_vulture(self) -> None:
        self.point_state = PointState.Vulture
        self.color = color.red

    def on_click(self) -> None:
        if self.point_state != PointState.Empty:
            print("Point not empty")
            return

        match state.turn:
            case Turn.Vulture:
                if state.num_vultures == 0:
                    self.to_vulture()
                    state.next_turn()
                else:
                    print("TODO")
            case Turn.Crow:
                if state.num_crows == state.MAX_CROWS:
                    print("TODO")
                else:
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
