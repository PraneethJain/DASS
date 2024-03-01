"""Script to generate random dataset"""

from random import choices, randint
import json

ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
Student = dict[str, list[int]]


def random_name(n: int) -> str:
    """Returns a random name of n letters"""
    return "".join(choices(ALPHABETS, k=n))


def random_scores(n: int) -> str:
    """Returns a list of random scores for n subjects"""
    return [randint(0, 100) for _ in range(n)]


def generate_random_dataset(
    num_students: int = 10, name_length: int = 5, num_subjets: int = 5
) -> list[Student]:
    """Returns a randomly generated dataset"""
    return [
        {random_name(name_length): random_scores(num_subjets)}
        for _ in range(num_students)
    ]


if __name__ == "__main__":
    dataset = generate_random_dataset()
    print(dataset)
    with open("dataset.json", "w") as f:
        json.dump(dataset, f)
