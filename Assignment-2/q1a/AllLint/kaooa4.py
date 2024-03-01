"""
Kaooa Game
"""

from enum import Enum, auto
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

    CROW = auto()
    VULTURE = auto()


class PointState(Enum):
    """What is the current state of the point"""

    EMPTY = auto()
    CROW = auto()
    VULTURE = auto()


class PointType(Enum):
    """Whether the point is in the inner pentagon or outer pentagon"""

    INNER = auto()
    OUTER = auto()


class Point(Sprite):
    """Main Point class"""

    outer_points = []
    inner_points = []

    def __init__(
        self,
        coords: tuple[float, float],
        point_type: PointType,
        index: int,
        is_dummy: bool = False,
    ) -> None:
        super().__init__(texture=None, model="circle", collider="sphere")
        self.point_state = PointState.EMPTY
        self.color = color.white
        self.scale = 0.3
        self.x = coords[0]
        self.y = coords[1]
        self.index = index
        self.point_type = point_type
        if not is_dummy:
            match self.point_type:
                case PointType.OUTER:
                    Point.outer_points.append(self)
                case PointType.INNER:
                    Point.inner_points.append(self)

    def get_scale(self) -> float:
        """get the scale"""
        return self.scale

    def set_scale(self, scale: float) -> float:
        """set the scale"""
        self.scale = scale

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
                lambda point: point.point_state == PointState.EMPTY,
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
            and Point.inner_points[idx].point_state == PointState.CROW
            for point in cls.empty_points()
        )

    def to_empty(self) -> None:
        """Convert self to empty"""
        self.point_state = PointState.EMPTY
        self.color = color.white
        self.scale = 0.3

    def to_crow(self) -> None:
        """Convert self to crow"""
        self.point_state = PointState.CROW
        self.color = color.green
        self.scale = 0.3

    def to_vulture(self) -> None:
        """Convert self to vulture"""
        self.point_state = PointState.VULTURE
        self.color = color.red
        self.scale = 0.3
        state.vulture_point = self

    def on_click(self) -> None:
        """Handle mouse clicks"""
        match state.turn:
            case Turn.VULTURE:
                if state.num_vultures == 0:
                    if self.point_state == PointState.EMPTY:
                        self.to_vulture()
                        state.next_turn()
                else:
                    match self.point_state:
                        case PointState.VULTURE:
                            # Ignore
                            pass
                        case PointState.CROW:
                            # Ignore
                            pass
                        case PointState.EMPTY:
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
                                    == PointState.CROW
                                ):
                                    Point.inner_points[crow_index].to_empty()
                                    state.vulture_point.to_empty()
                                    self.to_vulture()
                                    state.num_captured += 1
                                    state.next_turn()
            case Turn.CROW:
                if state.num_crows == state.max_crows:
                    match self.point_state:
                        case PointState.VULTURE:
                            # Ignore
                            pass
                        case PointState.CROW:
                            state.select_crow(self)
                        case PointState.EMPTY:
                            # Try to move selected point here
                            if state.move_possible_adjacent(self):
                                state.selected_crow.to_empty()
                                state.selected_crow = None
                                self.to_crow()
                                state.next_turn()
                else:
                    if self.point_state == PointState.EMPTY:
                        self.to_crow()
                        state.next_turn()


class State:
    """Global State of the game"""

    max_crows = 7

    def __init__(self) -> None:
        self.turn = Turn.CROW
        self.num_crows = 0
        self.num_vultures = 0
        self.num_captured = 0

        self.selected_crow = Point((100, 100), PointType.INNER, 10000, True)
        self.vulture_point = Point((100, 100), PointType.INNER, 10000, True)

        self.selected_crow = None
        self.vulture_point = None

        Point.reset()

    def reset(self) -> None:
        """Reset the game to its initial state"""
        self.turn = Turn.CROW
        self.num_crows = 0
        self.num_vultures = 0
        self.num_captured = 0

        self.selected_crow: None | Point = None
        self.vulture_point: None | Point = None

        Point.reset()

    def next_turn(self) -> None:
        """Progress the game by one turn"""

        def button_func():
            button.disable()
            self.reset()

        if self.num_captured == 4:
            button = Button("Vulture Wins!")

            button.on_click = button_func

        match self.turn:
            case Turn.CROW:
                if self.num_crows < self.max_crows:
                    self.num_crows += 1
                self.turn = Turn.VULTURE
                if self.vulture_point is not None:
                    self.vulture_point.set_scale(0.5)

                if self.vulture_point is not None and not Point.can_vulture_move():
                    button = Button("Kaooa Wins!")
                    button.on_click = button_func

            case Turn.VULTURE:
                self.vulture_point.set_scale(0.3)
                if self.num_vultures == 0:
                    self.num_vultures += 1
                self.turn = Turn.CROW

    def select_crow(self, crow: Point) -> None:
        """Selects and highlights the crow"""
        if self.selected_crow is not None:
            self.selected_crow.scale = 0.3
        self.selected_crow = crow
        self.selected_crow.scale = 0.5

    def move_possible_adjacent(self, end: Point) -> bool:
        """Checks whether it is possible to move adjacent"""
        if (self.turn == Turn.CROW and self.selected_crow is None) or (
            self.turn == Turn.VULTURE and self.vulture_point is None
        ):
            return False

        start = self.selected_crow if self.turn == Turn.CROW else self.vulture_point
        match start.point_type:
            case PointType.INNER:
                match end.point_type:
                    case PointType.INNER:
                        return end.index in (
                            (start.index - 1) % 5,
                            (start.index + 1) % 5,
                        )
                    case PointType.OUTER:
                        return end.index in (start.index, (start.index - 1) % 5)
            case PointType.OUTER:
                match end.point_type:
                    case PointType.INNER:
                        return end.index in (
                            start.index,
                            (start.index + 1) % 5,
                        )
                    case PointType.OUTER:
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
        if self.turn == Turn.CROW:
            raise RuntimeError("Capture only possible during vulture's turn")
        start = self.vulture_point
        res = None
        match start.point_type:
            case PointType.INNER:
                if end.point_type == PointType.OUTER:
                    if end.index == (start.index + 1) % 5:
                        res = end.index
                    if end.index == (start.index - 2) % 5:
                        res = (start.index - 1) % 5
            case PointType.OUTER:
                if end.point_type == PointType.INNER:
                    if end.index == (start.index - 1) % 5:
                        res = start.index
                    if end.index == (start.index + 2) % 5:
                        res = (start.index + 1) % 5
        return res


def construct_star() -> None:
    """Construct the initial board"""
    d = sin(126 * pi / 180) / sin(18 * pi / 180)
    _ = [
        Point((sin(2 * pi * i / 5), cos(2 * pi * i / 5)), PointType.INNER, i)
        for i in range(5)
    ]
    _ = [
        Point(
            (d * sin(2 * pi * i / 5 + pi / 5), d * cos(2 * pi * i / 5 + pi / 5)),
            PointType.OUTER,
            i,
        )
        for i in range(5)
    ]
    _ = [
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
