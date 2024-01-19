from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, Footer, Input, Static
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
import csv


class Database:
    def __init__(self, filepath: str = "data.csv") -> None:
        self.filepath = filepath
        self.load_data()

    def load_data(self) -> None:
        with open(self.filepath, newline="") as csvfile:
            self.data = list(csv.reader(csvfile, delimiter=" ", quotechar="|"))

    def save_data(self) -> None:
        with open(self.filepath, "w", newline="") as csvfile:
            csv.writer(
                csvfile, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            ).writerows(self.data)

    def add_data(self, data: list[str]) -> None:
        self.data.append(data)
        self.save_data()

    def remove_data(self, index: int) -> None:
        self.data = self.data[:index] + self.data[index + 1 :]
        self.save_data()

    def update_data(self, data: list[str], index: int) -> None:
        self.data[index] = data
        self.save_data()

    def get_headers(self) -> list[str]:
        return [
            "First Name",
            "Last Name",
            "Roll Number",
            "Course Name",
            "Semester",
            "Exam Type",
            "Total Marks",
            "Scored Marks",
        ]

    def get_data(self) -> list[list[str]]:
        return self.data


class InputEntry(Screen):
    def __init__(
        self,
        fields: list[str],
        operation: str,
        index: int | None = None,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.operation = operation
        match self.operation:
            case "insert":
                self.input_widgets = [Input(placeholder=field) for field in fields]
            case "update":
                self.input_widgets = [
                    Input(value=field, placeholder=field) for field in fields
                ]
                self.index = index
        self.input_widgets[2].type = "integer"  # Roll Number
        self.input_widgets[-1].type = "integer"  # Total Marks
        self.input_widgets[-2].type = "integer"  # Scored Marks

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return
        if event.button.id == "submit":
            match self.operation:
                case "insert":
                    db.add_data([wid.value for wid in self.input_widgets])
                case "update":
                    db.update_data(
                        [wid.value for wid in self.input_widgets], self.index
                    )
        self.app.pop_screen()
        table = self.app.query_one(DataTable)
        table.clear(True)
        table.add_columns(*db.get_headers())
        table.add_rows(db.get_data())

    def compose(self) -> ComposeResult:
        yield from self.input_widgets
        yield Button("Submit", id="submit")
        yield Button("Cancel", id="cancel")


class Search(Screen):
    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.input = Input(placeholder="Roll Number")
        self.results_table = DataTable(
            zebra_stripes=True, header_height=2, cursor_type="none"
        )
        self.results_table.add_columns(*db.get_headers())
        self.data = db.get_data()
        self.results_table.add_rows(self.data)

    @on(Input.Changed)
    def update_results_table(self, event: Input.Changed) -> None:
        current_data: list[list[str]] = []
        for row in self.data:
            if event.value in row[2]:  # if number entered is part of roll number
                current_data.append(row)
        self.results_table.clear()
        self.results_table.add_rows(current_data)

    def compose(self) -> ComposeResult:
        yield self.input
        yield self.results_table
        yield Static("Escape to close")


class Table(Screen):
    def compose(self) -> ComposeResult:
        with Horizontal(id="body"):
            yield DataTable(
                zebra_stripes=True,
                header_height=2,
                cursor_type="row",
            )

            with Vertical(id="operation-buttons"):
                yield Button("Insert", id="insert-button")
                yield Button("Update", id="update-button")
                yield Button("Delete", id="delete-button")
                yield Button("Search", id="search-button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        table = self.query_one(DataTable)
        match event.button.id:
            case "insert-button":
                self.app.push_screen(InputEntry(db.get_headers(), "insert"))
            case "update-button":
                self.app.push_screen(
                    InputEntry(
                        db.get_data()[table.cursor_row], "update", table.cursor_row
                    )
                )
            case "delete-button":
                db.remove_data(table.cursor_row)
            case "search-button":
                self.app.push_screen(Search())
        table.clear(True)
        table.add_columns(*db.get_headers())
        table.add_rows(db.get_data())

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*db.get_headers())
        table.add_rows(db.get_data())


class MarksDirectory(App[None]):
    CSS_PATH = "mdirectory.tcss"
    SCREENS = {}
    BINDINGS = [Binding("q", "quit", "Quit")]
    TITLE = "Marks Directory"

    def on_mount(self) -> None:
        self.push_screen(Table())


if __name__ == "__main__":
    db = Database()
    MarksDirectory().run()
