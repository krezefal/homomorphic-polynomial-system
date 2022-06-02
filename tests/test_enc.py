import sys
import unittest
import logging
import numpy as np

from cryptosystem.keygen import generate_abramov_keypair


class TestEncryption(unittest.TestCase):
    reference_base = 8
    reference_degree = 4

    @classmethod
    def setUpClass(cls):  # Keypair will be generated once for all these test cases
        cls.log = logging.getLogger("TestEncryption")
        cls.private_key, cls.public_key = \
            generate_abramov_keypair(cls.reference_base, cls.reference_degree)
        cls.test_number = 197

    def test_encoding(self):
        reference_polynomial = np.poly1d([3, 0, 5])
        test_polynomial = self.public_key.encode(self.test_number)

        self.log.debug(f"\nPolynomial for testing:\n{test_polynomial}\n")
        self.log.debug(f"\nReference polynomial:\n{reference_polynomial}\n")

        self.assertEqual(test_polynomial, reference_polynomial)

    def test_encryption(self):
        test_polynomial = self.public_key.encrypt(self.test_number)

        self.log.debug(f"\nEncrypted polynomial:\n{test_polynomial}\n")

        self.assertEqual("foo & bar", "foo & bar")

    def test_decryption(self):
        test_polynomial = self.public_key.encrypt(self.test_number)
        decrypted_test_number = self.private_key.decrypt(test_polynomial)

        self.log.debug(f"\nTesting value:\n{self.test_number}\n")
        self.log.debug(f"\nDecrypted value:\n{decrypted_test_number}\n")

        self.assertEqual(self.test_number, decrypted_test_number)


if __name__ == '__main__':
    # Change logging level from DEBUG to INFO to see less details
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    unittest.main(verbosity=2)
