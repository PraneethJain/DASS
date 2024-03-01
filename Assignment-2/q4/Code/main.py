"""Script to analyse student scores"""

Student = dict[str, list[int]]


def calculate_average(students: list[Student]) -> dict[str, float]:
    """Returns a dictionary of averages of each student"""
    res = {}
    for student in students:
        ((name, scores),) = student.items()
        res[name] = sum(scores) / len(scores)
    return res


def find_highest_scorer(students: list[Student]) -> tuple[str, list[str]]:
    """
    Returns a tuple containing:
    1. The name of the student with the highest average score
    2. Ordered list of student names who scored the highest in each corresponding subject
    """
    if not students:
        raise ValueError("expected non empty list of students")

    return (
        max(calculate_average(students).items(), key=lambda x: x[1])[0],
        [
            next(iter(max(students, key=lambda x: next(iter(x.values()))[i]).keys()))
            for i in range(len(next(iter(students[0].values()))))
        ],
    )


if __name__ == "__main__":
    students = [
        {"a": [1, 2, 300, 4]},
        {"b": [10, 20, 30, 40]},
        {"c": [1000, 17, 21, 39]},
    ]

    x = find_highest_scorer(students)
    print(x)
