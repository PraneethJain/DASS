"""Tests for Kaprekar Routine"""

import unittest
import sys

sys.path.insert(0, "..")
from Code.kaprekarroutine import kaprekar


class TestKaprekarRoutine(unittest.TestCase):
    """Test Case Class for Kaprekar Routine"""

    def test_valid_string_full(self):
        self.assertEqual(kaprekar("9218"), ["9218", "8532", "6174"])
        self.assertEqual(kaprekar("1234"), ["1234", "3087", "8352", "6174"])
        self.assertEqual(kaprekar("4321"), ["4321", "3087", "8352", "6174"])
        self.assertEqual(kaprekar("1190"), ["1190", "8991", "8082", "8532", "6174"])
        self.assertEqual(
            kaprekar("0001"), ["0001", "0999", "8991", "8082", "8532", "6174"]
        )

    def test_valid_string_partial(self):
        self.assertEqual(kaprekar("201"), ["0201", "2088", "8532", "6174"])
        self.assertEqual(
            kaprekar("1"), ["0001", "0999", "8991", "8082", "8532", "6174"]
        )

    def test_valid_int_full(self):
        self.assertEqual(kaprekar(9218), ["9218", "8532", "6174"])
        self.assertEqual(kaprekar(1234), ["1234", "3087", "8352", "6174"])
        self.assertEqual(kaprekar(4321), ["4321", "3087", "8352", "6174"])
        self.assertEqual(kaprekar(1190), ["1190", "8991", "8082", "8532", "6174"])

    def test_valid_int_partial(self):
        self.assertEqual(kaprekar(201), ["0201", "2088", "8532", "6174"])
        self.assertEqual(kaprekar(1), ["0001", "0999", "8991", "8082", "8532", "6174"])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            kaprekar(0)
        with self.assertRaises(ValueError):
            kaprekar("0")
        with self.assertRaises(ValueError):
            kaprekar(1111)
        with self.assertRaises(ValueError):
            kaprekar("1111")
        with self.assertRaises(ValueError):
            kaprekar("banana")
        with self.assertRaises(ValueError):
            kaprekar("12351")


if __name__ == "__main__":
    unittest.main()
