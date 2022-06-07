import secrets
import numpy as np

from .vars import *


def generate_obfuscating_multiplier(even_degree: int) -> np.poly1d:
    assert even_degree % 2 == 0, "Must be EVEN for the polynomial to have no rational roots"

    if even_degree != 0:
        coef_at_passed_deg = secrets.randbelow(MAX_COEFFICIENT_VALUE) + 1
        coef_at_zero_deg = secrets.randbelow(MAX_COEFFICIENT_VALUE) + 1
        obfuscating_polynomial = np.poly1d([coef_at_passed_deg, *(np.zeros(even_degree - 1)), coef_at_zero_deg])
        return obfuscating_polynomial
    else:
        coef_at_zero_deg = secrets.randbelow(MAX_COEFFICIENT_VALUE) + 1
        obfuscating_const = np.poly1d(coef_at_zero_deg)
        return obfuscating_const


def is_number(polynomial: np.poly1d) -> bool:
    if polynomial.order == 0:
        return True
    else:
        return False


def is_zero(polynomial: np.poly1d) -> bool:
    if polynomial.order == 0 and polynomial[0] == 0:
        return True
    else:
        return False
