"""Kaprekar Routine"""


def kaprekar(s: str | int) -> list[int]:
    """Computes the kaprekar routine

    Args:
        s (str): input number in string form with leading zeros if needed

    Raises:
        ValueError: input is invalid

    Returns:
        list[int]: The kaprekar sequence of the number
    """
    s = str(s).rjust(4, "0")
    if not (
        s.isdigit() and len(s) == 4 and s not in {"0000", "1111"} and len(set(s)) >= 2
    ):
        raise ValueError("Inappropriate input")

    res = [s]
    while True:
        prev = res[-1]
        inc = int("".join(sorted(prev)))
        dec = int("".join(sorted(prev, reverse=True)))
        cur = str(dec - inc).rjust(4, "0")
        if cur == prev:
            break
        res.append(cur)
    return res


if __name__ == "__main__":
    print(kaprekar(input()))
