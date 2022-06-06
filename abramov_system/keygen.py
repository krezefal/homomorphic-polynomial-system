from typing import Tuple
import secrets
import numpy as np

from .utils import generate_obfuscating_multiplier
from .vars import *


class AbramovPrivateKey:
    def __init__(self, root: float):
        self._root = root

    def decrypt(self, encrypted_number: np.poly1d) -> int:
        decrypted_number = np.polyval(encrypted_number, self._root)
        rounded_decrypted_number = np.round(decrypted_number, ROUND_ACCURACY)
        return int(rounded_decrypted_number)

    def get_root(self):
        return self._root


class AbramovPublicKey:
    def __init__(self, base: int, key_polynomial: np.poly1d):
        self._base = base
        self._key_polynomial = key_polynomial

    def encode(self, number: int) -> np.poly1d:
        in_new_numbering_system = np.base_repr(number, self._base)
        polynomial_representation = np.poly1d([int(digit) for digit in str(in_new_numbering_system)])
        return polynomial_representation

    def encrypt(self, number: int) -> np.poly1d:
        encoded_number = self.encode(number)
        encrypted_number = np.polyval(encoded_number, self._key_polynomial)
        return encrypted_number

    def get_base(self):
        return self._base

    def get_polynomial(self):
        return self._key_polynomial


def generate_abramov_keypair(base: int, polynomial_degree: int) -> Tuple[AbramovPrivateKey, AbramovPublicKey]:
    coef_at_first_deg = secrets.randbelow(MAX_COEFFICIENT_VALUE) + 1
    coef_at_zero_deg = secrets.randbelow(MAX_COEFFICIENT_VALUE) + 1
    key_polynomial = np.poly1d([coef_at_first_deg, coef_at_zero_deg])

    if polynomial_degree % 2 == 0:
        degree = polynomial_degree
    else:
        degree = polynomial_degree - 1

    while degree != 0:
        tmp_degree = secrets.randbelow(int(degree / 2)) + 1
        obfuscating_polynomial = generate_obfuscating_multiplier(2 * tmp_degree)
        key_polynomial = key_polynomial * obfuscating_polynomial
        degree -= tmp_degree * 2

    key_polynomial += base
    root = - coef_at_zero_deg / coef_at_first_deg

    private_key = AbramovPrivateKey(root)
    public_key = AbramovPublicKey(base, key_polynomial)

    return private_key, public_key
