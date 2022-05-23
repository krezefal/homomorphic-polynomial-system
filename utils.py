import secrets

import numpy as np
from numpy.polynomial import Polynomial


def generate_obfuscating_multiplier(even_degree, coef_max_val: int) -> Polynomial:
    if even_degree != 0:
        coef_at_passed_deg = secrets.randbelow(coef_max_val) + 1
        coef_at_zero_deg = secrets.randbelow(coef_max_val) + 1
        obfuscating_polynomial = Polynomial([coef_at_zero_deg, np.zeros(even_degree - 1), coef_at_passed_deg])
        return obfuscating_polynomial
    else:
        coef_at_zero_deg = secrets.randbelow(coef_max_val) + 1
        obfuscating_const = Polynomial(coef_at_zero_deg)
        return obfuscating_const
