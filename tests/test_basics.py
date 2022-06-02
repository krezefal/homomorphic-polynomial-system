import sys
import unittest
import logging
import numpy as np

from cryptosystem.utils import generate_obfuscating_multiplier
from cryptosystem.keygen import generate_abramov_keypair
from cryptosystem.vars import ROUND_ACCURACY


class TestUtils(unittest.TestCase):
    reference_degree = 4

    def setUp(self):
        self.log = logging.getLogger("TestUtils")
        self.test_polynomial = generate_obfuscating_multiplier(self.reference_degree)
        self.log.debug(f"\nPolynomial for testing:\n{self.test_polynomial}\n")

    def test_polynomial_generating_with_given_degree(self):
        self.log.debug(f"\nReference degree: {self.reference_degree}\n")
        self.assertEqual(self.test_polynomial.order, self.reference_degree)

    def test_polynomial_creating_with_no_rational_roots(self):
        roots = self.test_polynomial.r
        self.log.debug(f"\nRoots of the testing polynomial:\n{roots}\n")
        for root in np.nditer(roots):
            self.assertNotEqual(np.imag(root), 0)

    def test_polynomial_generating_with_zero_degree(self):
        zero_polynomial = generate_obfuscating_multiplier(0)
        self.log.debug(f"\nPolynomial with zero degree:\n{zero_polynomial}\n")
        self.assertEqual(zero_polynomial.order, 0)


class TestKeypairAttr(unittest.TestCase):
    reference_base = 8
    reference_degree = 4

    @classmethod
    def setUpClass(cls):  # Keypair will be generated once for all these test cases
        cls.log = logging.getLogger("TestKeypairAttr")
        cls.private_key, cls.public_key = \
            generate_abramov_keypair(cls.reference_base, cls.reference_degree)

    def test_private_key_is_float(self):
        self.log.debug(f"\nRoot (private key attr): {self.private_key.get_root()}\n")
        self.log.debug(f"\nType: {type(self.private_key.get_root())}\n")
        self.assertIsInstance(self.private_key.get_root(), float)

    def test_bases_equality(self):
        self.log.debug(f"\nBase (public key attr): {self.public_key.get_base()}\n")
        self.log.debug(f"\nReference base : {self.reference_base}\n")
        self.assertEqual(self.public_key.get_base(), self.reference_base)

    # According to the theory, key polynomial
    # must have only 1 rational root
    def test_key_polynomial_has_one_rational_root(self):
        key_polynomial = self.public_key.get_polynomial()
        self.log.debug(f"\nKey polynomial (public key attr):\n{key_polynomial}\n")

        roots = key_polynomial.r
        self.log.debug(f"\nRoots of the key polynomial:\n{roots}\n")

        amount_of_rational_roots = 0
        for root in np.nditer(roots):
            if np.imag(root) == 0:
                amount_of_rational_roots += 1

        self.assertEqual(amount_of_rational_roots, 1)

    # Degree of the key polynomial must be equal
    # to passed degree (or + 1 if it was set to even)
    def test_key_polynomial_has_proper_degree(self):
        key_polynomial = self.public_key.get_polynomial()
        self.log.debug(f"\nKey polynomial (public key attr):\n{key_polynomial}\n")
        self.log.debug(f"\nReference degree: {self.reference_degree}\n")

        if self.reference_degree % 2 == 0:
            self.assertEqual(key_polynomial.order, self.reference_degree + 1)
        else:
            self.assertEqual(key_polynomial.order, self.reference_degree)

    # Correctness of key polynomial is confirmed
    # when, after substituting its root into it,
    # the expression becomes equal to the base
    def test_key_polynomial_correctness(self):
        key_polynomial = self.public_key.get_polynomial()
        root = self.private_key.get_root()
        self.log.debug(f"\nKey polynomial (public key attr):\n{key_polynomial}\n")

        substitution_result = np.polyval(key_polynomial, root)
        rounded_result = np.round(substitution_result, ROUND_ACCURACY)
        self.log.debug(f"\nRounded substitution result: {rounded_result}\n")

        self.assertEqual(self.reference_base, rounded_result)


if __name__ == '__main__':
    # Change logging level from DEBUG to INFO to see less details
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)
