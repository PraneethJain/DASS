"""Script to show the nth Lucas Number"""

import sys


def lucas_number(n: int) -> int:
    """Returns the nth lucas number"""
    if n == 0:
        return -3
    if n == 1:
        return -1
    a, b = -3, -1
    while n:
        a, b = b, a + b
        n -= 1
    return a


if __name__ == "__main__":
    sys.set_int_max_str_digits(225000)
    print(lucas_number(int(input())))
