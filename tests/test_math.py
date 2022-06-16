import sys
import unittest
import logging
import numpy as np

from homomorphic_polynomial_system.keygen import generate_abramov_keypair
from homomorphic_polynomial_system.vars import ROUND_TO_INT, ROUND_TO_REAL_NUMBERS


class TestMath(unittest.TestCase):
    reference_base = 7
    reference_degree = 8

    @classmethod
    def setUpClass(cls):  # Keypair will be generated once for all these test cases
        cls.log = logging.getLogger("TestMath")
        cls.private_key, cls.public_key = \
            generate_abramov_keypair(cls.reference_base, cls.reference_degree)

        cls.test_number1 = 56
        cls.test_number2 = 112
        cls.test_small_number1 = 2
        cls.test_small_number2 = 3

        cls.encrypted_number1 = cls.public_key.encrypt(cls.test_number1)
        cls.encrypted_number2 = cls.public_key.encrypt(cls.test_number2)
        cls.encrypted_small_number1 = cls.public_key.encrypt(cls.test_small_number1)
        cls.encrypted_small_number2 = cls.public_key.encrypt(cls.test_small_number2)

    def test_addition(self):
        addition_result = self.test_number1 + self.test_number2
        enc_addition_result = self.encrypted_number1 + self.encrypted_number2
        dec_addition_result = self.private_key.decrypt(enc_addition_result)
        rounded_dec_addition_result = np.round(dec_addition_result, ROUND_TO_INT)

        self.log.debug(f"\nAddition result: {addition_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_addition_result}\n")

        self.assertEqual(addition_result, rounded_dec_addition_result)

    def test_subtraction(self):
        subtraction_result = self.test_number1 - self.test_number2
        enc_subtraction_result = self.encrypted_number1 - self.encrypted_number2
        dec_subtraction_result = self.private_key.decrypt(enc_subtraction_result)
        rounded_dec_subtraction_result = np.round(dec_subtraction_result, ROUND_TO_INT)

        self.log.debug(f"\nSubtraction result: {subtraction_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_subtraction_result}\n")

        self.assertEqual(subtraction_result, rounded_dec_subtraction_result)

    def test_multiplication(self):
        multiplication_result = self.test_number1 * self.test_number2
        enc_multiplication_result = self.encrypted_number1 * self.encrypted_number2
        dec_multiplication_result = self.private_key.decrypt(enc_multiplication_result)
        rounded_dec_multiplication_result = np.round(dec_multiplication_result, ROUND_TO_INT)

        self.log.debug(f"\nMultiplication result: {multiplication_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_multiplication_result}\n")

        self.assertEqual(multiplication_result, rounded_dec_multiplication_result)

    def test_division(self):
        division_result = self.test_number1 / self.test_number2
        rounded_division_result = np.round(division_result, ROUND_TO_REAL_NUMBERS)
        whole_part, remains, divider = self.encrypted_number1 / self.encrypted_number2

        dec_whole_part = self.private_key.decrypt(whole_part)
        dec_remains = self.private_key.decrypt(remains)
        dec_divider = self.private_key.decrypt(divider)

        dec_division_result = dec_whole_part + dec_remains / dec_divider
        rounded_dec_division_result = np.round(dec_division_result, ROUND_TO_REAL_NUMBERS)

        self.log.debug(f"\nDivision result: {rounded_division_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_division_result}\n")

        self.assertEqual(rounded_division_result, rounded_dec_division_result)

    def test_small_num_division(self):
        division_result = self.test_small_number1 / self.test_small_number2
        rounded_division_result = np.round(division_result, ROUND_TO_REAL_NUMBERS)
        whole_part, remains, divider = self.encrypted_small_number1 / self.encrypted_small_number2

        dec_whole_part = self.private_key.decrypt(whole_part)
        dec_remains = self.private_key.decrypt(remains)
        dec_divider = self.private_key.decrypt(divider)

        dec_division_result = dec_whole_part + dec_remains / dec_divider
        rounded_dec_division_result = np.round(dec_division_result, ROUND_TO_REAL_NUMBERS)

        self.log.debug(f"\nDivision result: {rounded_division_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_division_result}\n")

        self.assertEqual(rounded_division_result, rounded_dec_division_result)

    def test_norm_divisible_small_divider(self):
        division_result = self.test_number1 / self.test_small_number2
        rounded_division_result = np.round(division_result, ROUND_TO_REAL_NUMBERS)
        whole_part, remains, divider = self.encrypted_number1 / self.encrypted_small_number2

        dec_whole_part = self.private_key.decrypt(whole_part)
        dec_remains = self.private_key.decrypt(remains)
        dec_divider = self.private_key.decrypt(divider)

        dec_division_result = dec_whole_part + dec_remains / dec_divider
        rounded_dec_division_result = np.round(dec_division_result, ROUND_TO_REAL_NUMBERS)

        self.log.debug(f"\nDivision result: {rounded_division_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_division_result}\n")

        self.assertEqual(rounded_division_result, rounded_dec_division_result)

    def test_small_divisible_norm_divider(self):
        division_result = self.test_small_number1 / self.test_number2
        rounded_division_result = np.round(division_result, ROUND_TO_REAL_NUMBERS)
        whole_part, remains, divider = self.encrypted_small_number1 / self.encrypted_number2

        dec_whole_part = self.private_key.decrypt(whole_part)
        dec_remains = self.private_key.decrypt(remains)
        dec_divider = self.private_key.decrypt(divider)

        dec_division_result = dec_whole_part + dec_remains / dec_divider
        rounded_dec_division_result = np.round(dec_division_result, ROUND_TO_REAL_NUMBERS)

        self.log.debug(f"\nDivision result: {rounded_division_result}\n")
        self.log.debug(f"\nDecrypted result: {rounded_dec_division_result}\n")

        self.assertEqual(rounded_division_result, rounded_dec_division_result)


if __name__ == '__main__':
    # Change logging level from DEBUG to INFO to see less details
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)
