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


def main() -> None:
    students = []
    n = -1
    while n <= 0:
        try:
            n = int(input("Number of subjects: "))
        except ValueError as e:
            print(e)

    while True:
        name = input("Enter student name (empty to stop): ")
        if not name:
            break

        scores = []
        while not scores:
            print("Enter space separted integer scores")
            try:
                scores = list(map(int, input().split()))
            except ValueError as e:
                print(e)

        students.append({name: scores})

    averages = calculate_average(students)
    (highest_average_scorer, subject_highests) = find_highest_scorer(students)

    print()
    print(f"The averages of the students are: {averages}")
    print(f"The highest average scorer is {highest_average_scorer}")
    print(f"The subject wise highest scorers in order are {subject_highests}")


if __name__ == "__main__":
    main()
