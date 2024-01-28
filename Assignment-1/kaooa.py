from ursina import *
from enum import Enum, auto

app = Ursina()

window.color = color.black
camera.orthographic = True
camera.fov = 6


class Turn(Enum):
    Crow = auto()
    Vulture = auto()


class PointState(Enum):
    Empty = auto()
    Crow = auto()
    Vulture = auto()


class PointType(Enum):
    Inner = auto()
    Outer = auto()


class Point(Sprite):
    outer_points = []
    inner_points = []

    def __init__(self, x: float, y: float, point_type: PointType, index: int) -> None:
        super().__init__(texture=None, model="circle", collider="sphere")
        self.to_empty()
        self.x = x
        self.y = y
        self.index = index
        self.point_type = point_type
        match self.point_type:
            case PointType.Outer:
                Point.outer_points.append(self)
            case PointType.Inner:
                Point.inner_points.append(self)

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
        self.scale = 0.3
        state.vulture_point = self

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
                            if state.move_possible_adjacent(self):
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
                            state.select_crow(self)
                        case PointState.Empty:
                            # Try to move selected point here
                            if state.move_possible_adjacent(self):
                                state.selected_crow.to_empty()
                                state.selected_crow = None
                                self.to_crow()
                                state.next_turn()
                else:
                    if self.point_state == PointState.Empty:
                        self.to_crow()
                        state.next_turn()


class State:
    def __init__(self) -> None:
        self.turn = Turn.Crow
        self.num_crows = 0
        self.num_vultures = 0
        self.MAX_CROWS = 3

        self.selected_crow: None | Point = None
        self.vulture_point: None | Point = None

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

    def select_crow(self, crow: Point) -> None:
        if self.selected_crow is not None:
            self.selected_crow.scale = 0.3
        self.selected_crow = crow
        self.selected_crow.scale = 0.5

    def move_possible_adjacent(self, end: Point) -> bool:
        if (self.turn == Turn.Crow and self.selected_crow is None) or (
            self.turn == Turn.Vulture and self.vulture_point is None
        ):
            return False

        start = self.selected_crow if self.turn == Turn.Crow else self.vulture_point
        match start.point_type:
            case PointType.Inner:
                match end.point_type:
                    case PointType.Inner:
                        return end.index in (
                            (start.index - 1) % 5,
                            (start.index + 1) % 5,
                        )
                    case PointType.Outer:
                        return end.index in (start.index, (start.index - 1) % 5)
            case PointType.Outer:
                match end.point_type:
                    case PointType.Inner:
                        return end.index in (
                            start.index,
                            (start.index + 1) % 5,
                        )
                    case PointType.Outer:
                        return False


if __name__ == "__main__":
    state = State()
    d = sin(126 * pi / 180) / sin(18 * pi / 180)
    [
        Point(sin(2 * pi * i / 5), cos(2 * pi * i / 5), PointType.Inner, i)
        for i in range(5)
    ]
    [
        Point(
            d * sin(2 * pi * i / 5 + pi / 5),
            d * cos(2 * pi * i / 5 + pi / 5),
            PointType.Outer,
            i,
        )
        for i in range(5)
    ]
    lines = [
        Sprite(
            model="line",
            position=(
                (Point.outer_points[i].x + Point.outer_points[(i + 2) % 5].x) / 2,
                (Point.outer_points[i].y + Point.outer_points[(i + 2) % 5].y) / 2,
                1,
            ),
            rotation=(0, 0, 72 * (i - 1)),
            scale=distance_2d(Point.outer_points[0], Point.outer_points[2]),
        )
        for i in range(5)
    ]
    app.run()
