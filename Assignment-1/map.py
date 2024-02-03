from manim import *
from math import sqrt
from collections.abc import Generator


class Walk(Scene):
    @staticmethod
    def parse_directions(
        unparsed_directions: list[tuple[str, str]]
    ) -> Generator[tuple[float, float, float]]:
        for dir in unparsed_directions:
            multiplier = 0.2
            match dir[0][-2:]:
                case "mm":
                    multiplier *= 1
                case "cm":
                    multiplier *= 10
                case _:
                    raise Exception("Invalid unit found. Expected mm or cm")
            scale = float(dir[0][:-2])
            match dir[1]:
                case "N":
                    yield UP * scale * multiplier
                case "E":
                    yield RIGHT * scale * multiplier
                case "W":
                    yield LEFT * scale * multiplier
                case "S":
                    yield DOWN * scale * multiplier
                case "NE":
                    yield UR * scale * multiplier / sqrt(2)
                case "NW":
                    yield UL * scale * multiplier / sqrt(2)
                case "SE":
                    yield DR * scale * multiplier / sqrt(2)
                case "SW":
                    yield DL * scale * multiplier / sqrt(2)

    def construct(self):
        zoom = 0.5

        with open("./map.txt") as f:
            directions_unparsed = [line.strip().split() for line in f.readlines()]
        origin = Dot(radius=DEFAULT_DOT_RADIUS * zoom)
        dot = Dot(radius=DEFAULT_DOT_RADIUS * 2 * zoom, color=WHITE)
        self.play(Write(origin))
        self.play(Write(dot))
        text = Text("", font_size=zoom * DEFAULT_FONT_SIZE / 1.5).to_edge(UP)
        lines = []
        for dir_text, dir in zip(
            directions_unparsed, self.parse_directions(directions_unparsed)
        ):
            dir *= zoom
            self.wait(0.5)
            line = Line(dot.get_center(), dot.get_center() + dir, color=WHITE)
            lines.append(line)
            self.play(
                Write(line),
                Transform(
                    text,
                    Text(
                        f"{dir_text[0]} {dir_text[1]}",
                        font_size=zoom * DEFAULT_FONT_SIZE / 1.5,
                    ).to_edge(UP),
                ),
            )

            self.play(dot.animate.shift(dir))
        self.play(*[FadeOut(line) for line in lines], FadeOut(text))
        self.wait()

        final_line = Line(origin.get_center(), dot.get_center(), color=WHITE)
        diff = dot.get_center() - origin.get_center()
        direction_string = ""
        if diff[0] > 0:
            if diff[1] > 0:
                direction_string = "North East"
            elif diff[1] < 0:
                direction_string = "South East"
            else:
                direction_string = "East"
        elif diff[0] < 0:
            if diff[1] > 0:
                direction_string = "North West"
            elif diff[1] < 0:
                direction_string = "South West"
            else:
                direction_string = "West"
        else:
            if diff[1] > 0:
                direction_string = "North"
            elif diff[1] < 0:
                direction_string = "South"
            else:
                direction_string = "No Movement!"
        distance = Text(
            f"{round(final_line.get_length()/(zoom*0.2), 2)} mm {direction_string}",
            font_size=zoom * DEFAULT_FONT_SIZE,
        ).to_edge(DOWN)
        self.play(Write(final_line))
        self.play(Wiggle(final_line), Write(distance))

        self.wait()
