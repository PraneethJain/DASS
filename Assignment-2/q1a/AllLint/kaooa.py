"""
Kaooa Game
"""

from ursina import (
    Button,
    camera,
    color,
    cos,
    distance_2d,
    pi,
    sin,
    Sprite,
    Ursina,
    Vec2,
    window,
)
from enum import Enum, auto

app = Ursina(
    title="Kaooa",
    icon="vulture.ico",
    borderless=False,
    development_mode=False,
    size=Vec2(1000, 800),
)

window.color = color.black
camera.orthographic = True
camera.fov = 6


class Turn(Enum):
    """Whose turn it currently is"""

    Crow = auto()
    Vulture = auto()


class PointState(Enum):
    """What is the current state of the point"""

    Empty = auto()
    Crow = auto()
    Vulture = auto()


class PointType(Enum):
    """Whether the point is in the inner pentagon or outer pentagon"""

    Inner = auto()
    Outer = auto()


class Point(Sprite):
    """Main Point class"""

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

    @classmethod
    def reset(cls) -> None:
        """Resets all the points"""
        for point in cls.outer_points + cls.inner_points:
            point.to_empty()

    @classmethod
    def empty_points(cls):
        """Returns a list of empty points"""
        return list(
            filter(
                lambda point: point.point_state == PointState.Empty,
                cls.outer_points + cls.inner_points,
            )
        )

    @classmethod
    def can_vulture_move(cls) -> bool:
        """Checks if the vulture can move"""
        return cls.can_vulture_move_capture() or cls.can_vulture_move_adjacent()

    @classmethod
    def can_vulture_move_adjacent(cls) -> bool:
        """Checks if the vulture can move adjacent"""
        return any(state.move_possible_adjacent(point) for point in cls.empty_points())

    @classmethod
    def can_vulture_move_capture(cls) -> bool:
        """Checks if the vulture can capture"""
        return any(
            (idx := state.move_possible_capture(point)) is not None
            and Point.inner_points[idx].point_state == PointState.Crow
            for point in cls.empty_points()
        )

    def to_empty(self) -> None:
        """Convert self to empty"""
        self.point_state = PointState.Empty
        self.color = color.white
        self.scale = 0.3

    def to_crow(self) -> None:
        """Convert self to crow"""
        self.point_state = PointState.Crow
        self.color = color.green
        self.scale = 0.3

    def to_vulture(self) -> None:
        """Convert self to vulture"""
        self.point_state = PointState.Vulture
        self.color = color.red
        self.scale = 0.3
        state.vulture_point = self

    def on_click(self) -> None:
        """Handle mouse clicks"""
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
                            # Ignore
                            pass
                        case PointState.Empty:
                            # Try to move vulture here
                            if (
                                state.move_possible_adjacent(self)
                                and not self.can_vulture_move_capture()
                            ):
                                state.vulture_point.to_empty()
                                self.to_vulture()
                                state.next_turn()
                            # Or capture a crow in between
                            elif (
                                crow_index := state.move_possible_capture(self)
                            ) is not None:
                                if (
                                    Point.inner_points[crow_index].point_state
                                    == PointState.Crow
                                ):
                                    Point.inner_points[crow_index].to_empty()
                                    state.vulture_point.to_empty()
                                    self.to_vulture()
                                    state.num_captured += 1
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
    """Global State of the game"""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        """Reset the game to its initial state"""
        self.turn = Turn.Crow
        self.num_crows = 0
        self.num_vultures = 0
        self.MAX_CROWS = 7
        self.num_captured = 0

        self.selected_crow: None | Point = None
        self.vulture_point: None | Point = None

        Point.reset()

    def next_turn(self) -> None:
        """Progress the game by one turn"""
        if self.num_captured == 4:
            button = Button("Vulture Wins!")

            def ok():
                button.disable()
                self.reset()

            button.on_click = ok

        match self.turn:
            case Turn.Crow:
                if self.num_crows < self.MAX_CROWS:
                    self.num_crows += 1
                self.turn = Turn.Vulture
                if self.vulture_point is not None:
                    self.vulture_point.scale = 0.5

                if self.vulture_point is not None and not Point.can_vulture_move():
                    button = Button("Kaooa Wins!")

                    def ok():
                        button.disable()
                        self.reset()

                    button.on_click = ok

            case Turn.Vulture:
                self.vulture_point.scale = 0.3
                if self.num_vultures == 0:
                    self.num_vultures += 1
                self.turn = Turn.Crow

    def select_crow(self, crow: Point) -> None:
        """Selects and highlights the crow"""
        if self.selected_crow is not None:
            self.selected_crow.scale = 0.3
        self.selected_crow = crow
        self.selected_crow.scale = 0.5

    def move_possible_adjacent(self, end: Point) -> bool:
        """Checks whether it is possible to move adjacent"""
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

    def move_possible_capture(self, end: Point) -> int | None:
        """Checks if moving to end is possible while capturing a crow

        Args:
            end (Point): end point to move to

        Raises:
            Exception: if called during crow's turn

        Returns:
            int | None: index of captured crow, None if no capture possible
        """
        if self.turn == Turn.Crow:
            raise Exception("Capture only possible during vulture's turn")
        start = self.vulture_point
        match start.point_type:
            case PointType.Inner:
                match end.point_type:
                    case PointType.Inner:
                        return None
                    case PointType.Outer:
                        if end.index == (start.index + 1) % 5:
                            return end.index
                        elif end.index == (start.index - 2) % 5:
                            return (start.index - 1) % 5
                        else:
                            return None
            case PointType.Outer:
                match end.point_type:
                    case PointType.Inner:
                        if end.index == (start.index - 1) % 5:
                            return start.index
                        elif end.index == (start.index + 2) % 5:
                            return (start.index + 1) % 5
                        else:
                            return None
                    case PointType.Outer:
                        return None


def construct_star() -> None:
    """Construct the initial board"""
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
    [
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


if __name__ == "__main__":
    state = State()
    construct_star()
    app.run()
