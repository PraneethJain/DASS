from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, Input
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

    def remove_data(self, data: list[str]) -> None:
        self.data = list(filter(lambda d: d != data, self.data))
        self.save_data()

    def update_data(self, old_data: list[str], new_data: list[str]) -> None:
        for i, d in enumerate(self.data):
            if d == old_data:
                self.data[i] = new_data
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
    ) -> None:
        super().__init__(name=None, id="Input", classes=None)
        self.operation = operation
        match self.operation:
            case "insert":
                self.input_widgets = [Input(placeholder=field) for field in fields]
            case "update":
                self.old_data = fields
                self.input_widgets = [
                    Input(value=field, placeholder=field) for field in fields
                ]
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
                        self.old_data, [wid.value for wid in self.input_widgets]
                    )
        self.app.pop_screen()
        table = self.app.query_one(DataTable)
        table.clear(True)
        table.add_columns(*db.get_headers())
        table.add_rows(db.get_data())

    def compose(self) -> ComposeResult:
        yield from self.input_widgets
        with Horizontal(id="buttons"):
            yield Button("Submit", id="submit")
            yield Button("Cancel", id="cancel")


class Table(Screen):
    def __init__(self) -> None:
        super().__init__(name=None, id=None, classes=None)
        self.datatable = DataTable(header_height=2, cursor_type="row")
        self.search_input = Input(placeholder="Search any field")

    def compose(self) -> ComposeResult:
        with Vertical(id="body"):
            with Horizontal(id="operations"):
                yield self.search_input
                yield Button("Insert", id="insert-button")
                yield Button("Update", id="update-button")
                yield Button("Delete", id="delete-button")
            yield self.datatable

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        match event.button.id:
            case "insert-button":
                self.app.push_screen(InputEntry(db.get_headers(), "insert"))
            case "update-button":
                self.app.push_screen(
                    InputEntry(
                        self.datatable.get_row_at(self.datatable.cursor_row), "update"
                    )
                )
            case "delete-button":
                db.remove_data(self.datatable.get_row_at(self.datatable.cursor_row))

        self.update_table()

    @on(Input.Changed)
    def update_datatable(self, _: Input.Changed) -> None:
        self.update_table()

    def update_table(self) -> None:
        self.datatable.clear()
        self.datatable.add_rows(
            list(
                filter(
                    lambda row: any(self.search_input.value in val for val in row),
                    db.get_data(),
                ),
            )
        )

    def on_mount(self) -> None:
        self.datatable.add_columns(*db.get_headers())
        self.datatable.add_rows(db.get_data())


class MarksDirectory(App[None]):
    CSS_PATH = "mdirectory.tcss"
    SCREENS = {}
    BINDINGS = [Binding("escape", "quit", "Quit")]
    TITLE = "Marks Directory"

    def on_mount(self) -> None:
        self.push_screen(Table())


if __name__ == "__main__":
    db = Database()
    MarksDirectory().run()
