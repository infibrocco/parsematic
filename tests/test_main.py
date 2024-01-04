import unittest

from yampy import MathParser


class TestParse(unittest.TestCase):
    def setUp(self):
        self.parser = MathParser()

    def test_parse_with_addition_expression(self):
        expression = "2 + 3"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_subtraction_expression(self):
        expression = "5 - 3"
        expected_result = 2
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_multiplication_expression(self):
        expression = "4 * 5"
        expected_result = 20
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_division_expression(self):
        expression = "10 / 2"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_complex_expression(self):
        expression = "2 + 3 * 4 - 6 / 2"
        expected_result = 11
        result = self.parser.parse(expression)
        self.assertEqual(result, eval(expression))

    def test_parse_with_empty_expression(self):
        expression = ""
        expected_result = 0
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_whitespace_expression(self):
        expression = "   "
        expected_result = 0
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_single_number_expression(self):
        expression = "5"
        expected_result = 5
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_invalid_expression(self):
        expression = "2 +"
        with self.assertRaises(Exception):
            self.parser.parse(expression)

    def test_parse_with_negative_numbers(self):
        expression = "-5 + 3"
        expected_result = -2
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)

    def test_parse_with_powers(self):
        expression = "2 ** 3"
        expected_result = 8
        result = self.parser.parse(expression)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
