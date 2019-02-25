import unittest
from pazaak.helpers.utilities import first_true


class UtilitiesTest(unittest.TestCase):

    def test_first_true_basic(self):
        values = [False, False, True, False]
        result = first_true(values)
        self.assertTrue(result)

    def test_first_true_with_concrete_values(self):
        expected = 4
        values = [1, 2, 3, 4, 5]
        result = first_true(values, lambda x: x == expected)
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    def test_first_true_when_none_true(self):
        values = [1, 2, 3, 4, 5]
        result = first_true(values, lambda x: type(x) is str)
        self.assertIsNone(result)

    def test_first_true_with_default_value(self):
        default_value = -1
        values = [1, 2, 3, 4, 5]
        result = first_true(values, lambda x: x > 100, default=default_value)
        self.assertIsNotNone(result)
        self.assertEqual(default_value, result)


if __name__ == '__main__':
    unittest.main()