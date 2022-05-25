import sys
import unittest
import logging
import numpy as np

from utils import generate_obfuscating_multiplier
import cryptosystem as crypto


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.log = logging.getLogger("TestUtils")
        self.test_polynomial = generate_obfuscating_multiplier(4)

        self.log.debug(f"\nPolynomial for testing:\n{self.test_polynomial}\n")

    def test_the_generating_polynomial_with_given_degree(self):
        reference_polynomial = np.poly1d([1, 0, 0, 0, 1])
        self.assertEqual(reference_polynomial.order, self.test_polynomial.order)

        self.log.debug(f"\nThe reference polynomial:\n{reference_polynomial}\n")

    def test_the_producing_polynomial_with_no_rational_roots(self):
        roots = self.test_polynomial.r
        for root in np.nditer(roots):
            self.assertNotEqual(np.imag(root), 0)

        self.log.debug(f"\nRoots of the test polynomial:\n{roots}\n")


# class TestCryptoSystem(unittest.TestCase):
#
#     def test_sum_array(self):
#         self.assertEqual(array_sum([13, 2, 4, 5, 6]), 13 + 2 + 4 + 5 + 6)
#         self.assertEqual(array_sum([13, "test", 32, 4]), 0)
#
#
# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(WidgetTestCase('test_default_widget_size'))
#     suite.addTest(WidgetTestCase('test_widget_resize'))
#     return suite


if __name__ == '__main__':

    # Change logging level to DEBUG to see the details

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    unittest.main(verbosity=2)
