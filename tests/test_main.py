"""Tests for yampy
"""

import unittest

from yampy import MathParser


class TestParse(unittest.TestCase):
    """A unittest.TestCase class"""

    def setUp(self):
        """
        Set up the test case by initializing the MathParser object.

        Parameters:
            self (TestCase): The current test case object.
        """
        self.parser = MathParser()

    def test_parse_with_addition_expression(self):
        """
        Test the parsing of an addition expression.

        This function tests the functionality of the `parse` method in the `Parser` class by passing in an addition expression
        and checking if the result matches the expected value.

        Parameters:
        - self: The `ParserTest` instance.
        """
        expression = "2 + 3"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_subtraction_expression(self):
        """
        Test the parse_with_subtraction_expression function.

        This function tests the functionality of the parse_with_subtraction_expression
        method of the TestClass class. It verifies that the method correctly parses a subtraction
        expression and returns the expected result.

        Parameters:
        self (TestClass): An instance of the TestClass class.
        """
        expression = "5 - 3"
        expected_result = 2
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_multiplication_expression(self):
        """
        Test the `parse` method with a multiplication expression.

        This test case checks if the `parse` method of the `parser` object correctly evaluates a multiplication expression.

        Parameters:
        - expression (str): The expression to be parsed.
        """
        expression = "4 * 5"
        expected_result = 20
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_division_expression(self):
        """
        Test the parsing of a division expression.

        This function tests the parser's ability to correctly parse a division expression.
        It sets up a division expression "10 / 2" and expects the result to be 5.
        The function then calls the `parse` method of the `parser` object
        and asserts that the returned result is equal to the expected result.

        Parameters:
        - self: The instance of the test case class.
        """
        expression = "10 / 2"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_complex_expression(self):
        """
        Test the parsing of a complex expression.

        This function tests the parser's ability to correctly parse a complex expression
        containing addition, subtraction, multiplication, and division.
        It expects the result to match the expected value.

        Parameters:
        - expression (str): The complex expression to be parsed.
        """

        expression = "2 + 3 * 4 - 6 / 2"
        expected_result = 11
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_empty_expression(self):
        """
        Test the parsing of an empty expression.

        This function tests the parser's ability to handle an empty expression.
        It expects the result to be 0.
        """

        expression = ""
        expected_result = 0
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_whitespace_expression(self):
        """
        Test the parsing of a whitespace expression.

        This function tests the parser's ability to handle a whitespace expression.
        It expects the result to be 0.
        """

        expression = "   "
        expected_result = 0
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_single_number_expression(self):
        """
        Test the parsing of a single number expression.

        This function tests the parser's ability to correctly parse a single number expression.
        It expects the result to be the same as the parsed number.

        Parameters:
        - expression (str): The single number expression to be parsed.
        """

        expression = "5"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_invalid_expression(self):
        """
        Test the parsing of an invalid expression.

        This function tests the parser's ability to handle an invalid expression.
        It expects the parser to raise an exception.

        Parameters:
        - expression (str): The invalid expression to be parsed.
        """

        expression = "2 +"
        with self.assertRaises(Exception):
            self.parser.parse(expression)

    def test_parse_with_negative_numbers(self):
        """
        Test the parse method by passing an expression with negative numbers.

        The parse method of the Parser class is responsible for parsing the given expression and returning the result.
        This test case checks if the method can correctly parse an expression with negative numbers.

        Parameters:
        - self: The instance of the TestParser class.
        """
        expression = "-5 + 3"
        expected_result = -2
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_powers(self):
        """
        Test the parse method by passing an expression with powers.

        This test case verifies that the parser correctly evaluates expressions
        involving the exponentiation operator (**).

        Params:
            self (TestCase): The current test case.
        """
        expression = "2 ** 3"
        expected_result = 8
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
