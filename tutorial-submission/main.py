"""
Tutorial Submission
"""


def solve(inp: list[int]) -> int:
    """
    Finds the sum of the contiguous sublist with the largest sum within the given list
    """
    cur = inp[0]
    res = inp[0]

    for x in inp[1:]:
        cur = max(x, cur + x)
        res = max(res, cur)

    return res


if __name__ == "__main__":
    arr = list(map(int, input().split()))
    print(solve(arr))
