"""
Script to find all palindromes in a given year
"""

from datetime import date, timedelta


def palindrome(year: int) -> str:
    """Returns the palindrome date of the given year, or informs if none are found"""

    if year <= 0:
        raise ValueError("year must be positive")
    cur_date = date(year, 1, 1)
    end_date = date(year + 1, 1, 1)
    delta = timedelta(days=1)

    def is_palindrome(x: str):
        return x == x[::-1]

    while cur_date < end_date:
        if is_palindrome(f"{cur_date.day:02}{cur_date.month:02}{cur_date.year:04}"):
            return f"{cur_date.day:02}-{cur_date.month:02}-{cur_date.year:04}"
        cur_date += delta

    return "No Palindrome days available in the given year"


if __name__ == "__main__":
    print(palindrome(int(input())))
