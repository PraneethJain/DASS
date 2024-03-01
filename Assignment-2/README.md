# DASS Assignment 2

## q1a

- The initial pylint score was 3.48, mainly due to wild card imports and lack of doc-strings
- After removing wild card imports and adding doc-strings, in iteration 1, the score improved to 4.94
- After renaming variables to follow conventions and combining return values, in iteration 2, the score improved to 6.43
- After removing a double definition of a function and creating all instance variables in the init function, in iteration 3, the score improved to 6.89
- After redefining types for optional variables that can be None and combining coordinates into tuples, in iteration 4 (final), the score improved to 10.0

## q1b

- Since the test case has large values of n, the maximum printing limit of the system has to be increased in order for the number to be printed
- This is done using the sys module
- The file has been renamed from Lucasinitial.py to lucasinitial.py in accordance with pylint specifications
- The pylint score was a 10.0

## q2

To run the routine, `python3 kaprekarroutine.py` in the Code directory

To run the tests, `python3 test_kaprekarroutine.py` in the testcases directory

- The function is implemented to handle both string and integer inputs
- In case the given input is not valid, a `ValueError` is raised
- Multiple test case sets have been created
- Firstly, valid 4 length strings are checked
- Then, valid strings which need to be padded are checked
- Then, the above two types of tests are run for integers
- Finally, invalid cases are checked to raise `ValueError`

## q3

To run the tests, `pytest` in the testcases directory

- Since it is a lot of manual casework to check for leap years and number of dates in a month, the built-in `datetime` library has been used to enumerate all the valid dates in an year
- This leads to no edge cases in case of leap years and calendar changes
- The tests first test for valid cases, then tests for cases not found, then tests for cases where the input is out of bounds

## q4
To run the main code, `python3 main.py` in the Code directory

To generate a new random dataset, `python3 gen.py` in the Dataset directory

To run the test cases, `pytest` in the testcases directory

- After generating the dataset, it is stored in a `json` file. It is then imported in the main code, and the user is prompted for additional students to add
- The tests for average and highest use multiple students with varying subjects
- ValueError is raised when an empty list is passed when finding the highest scorer
- It is assumed that the number of subjects are constant across all students