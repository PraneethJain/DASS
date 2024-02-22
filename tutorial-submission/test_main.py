from main import solve


def test_solve_one_negative():
    assert solve([-5]) == -5


def test_solve_all_negative():
    assert solve([-1, -2, -10, -20, -5]) == -1


def test_solve_one_positive():
    assert solve([10]) == 10


def test_solve_all_positive():
    assert solve([1, 2, 3, 4, 5]) == 15


def test_solve_mixed():
    assert solve([1, -1, 10, -20, 40]) == 40
