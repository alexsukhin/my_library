from django.test import TestCase

from parameterized import parameterized

from loans.helpers import is_prime

class IsPrimeTestCase(TestCase):

    @parameterized.expand([
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (7, True),
        (9, False),
        (11, True),
        (15, False),
        (27, False),
        (49, False),
        (2017, True),
        (2117, False),
    ])

    def test_is_prime_with_positive_integer(self, number, expected_result):
        actual_result = is_prime(number)
        self.assertEqual(expected_result, actual_result)

    @parameterized.expand([
        (-7,),
        (0,),
        (3.5,), 
        ("eleven",),
    ])
    
    def test_invalid_inputs_raise_value_error(self, value):
        with self.assertRaises(ValueError):
            is_prime(value)