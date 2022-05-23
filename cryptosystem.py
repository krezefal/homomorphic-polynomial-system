from typing import Tuple
import secrets
import numpy as np

from utils import generate_obfuscating_multiplier


class AbramovPrivateKey:
    def __init__(self, root: float):
        self.root = root

    def decrypt(self, encrypted_number: np.poly1d) -> float:
        decrypted_number = np.polyval(encrypted_number, self.root)
        return float(decrypted_number)


class AbramovPublicKey:
    def __init__(self, base: int, key_polynomial: np.poly1d):
        self.base = base
        self.key_polynomial = key_polynomial

    def encode(self, number: int) -> np.poly1d:
        in_new_numbering_system = np.base_repr(number, self.base)
        polynomial_representation = np.poly1d(map(int, str(in_new_numbering_system)))
        return polynomial_representation

    def encrypt(self, number: int) -> np.poly1d:
        encoded_number = self.encode(number)
        encrypted_number = np.polyval(encoded_number, self.key_polynomial)
        return encrypted_number


def generate_abramov_keypair(degree, base, coef_max_val: int) -> Tuple[AbramovPrivateKey, AbramovPublicKey]:
    coef_at_first_deg = secrets.randbelow(coef_max_val) + 1
    coef_at_zero_deg = secrets.randbelow(coef_max_val) + 1
    key_polynomial = np.poly1d([coef_at_first_deg, coef_at_zero_deg + base])

    if degree % 2 != 0:
        degree -= 1

    while degree != 0:
        tmp_degree = secrets.randbelow(degree / 2)
        obfuscating_polynomial = generate_obfuscating_multiplier(2 * tmp_degree, coef_max_val)
        key_polynomial = key_polynomial * obfuscating_polynomial
        degree -= tmp_degree * 2

    root = - coef_at_zero_deg / coef_at_first_deg

    private_key = AbramovPrivateKey(root)
    public_key = AbramovPublicKey(base, key_polynomial)

    return private_key, public_key
