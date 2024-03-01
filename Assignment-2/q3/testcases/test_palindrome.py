import pytest
import sys

sys.path.insert(0, "..")
from Code.palindrome import palindrome


def test_found():
    assert palindrome(2001) == "10-02-2001"
    assert palindrome(2002) == "20-02-2002"
    assert palindrome(2010) == "01-02-2010"
    assert palindrome(2011) == "11-02-2011"
    assert palindrome(2012) == "21-02-2012"


def test_not_found():
    assert palindrome(2000) == "No Palindrome days available in the given year"
    assert palindrome(2005) == "No Palindrome days available in the given year"


def test_invalid():
    with pytest.raises(ValueError):
        palindrome(-1)
    with pytest.raises(ValueError):
        palindrome(0)
    with pytest.raises(ValueError):
        palindrome(100000)
