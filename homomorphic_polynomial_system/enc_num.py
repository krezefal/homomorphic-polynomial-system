import numpy as np

from .utils import is_zero, is_number


class EncryptedNumber:
    def __init__(self, polynomial: np.poly1d):
        self.polynomial = polynomial

    def __str__(self):
        return self.polynomial.__str__()

    def __add__(self, other):
        result = EncryptedNumber(self.polynomial + other.polynomial)
        return result

    def __mul__(self, other):
        result = EncryptedNumber(self.polynomial * other.polynomial)
        return result

    def __sub__(self, other):
        result = EncryptedNumber(self.polynomial - other.polynomial)
        return result

    def __truediv__(self, other):
        if is_zero(other.polynomial):
            raise ZeroDivisionError()

        enc_q, enc_r = self.polynomial / other.polynomial

        if is_number(self.polynomial) and is_number(other.polynomial):
            result = EncryptedNumber(enc_q)
            zero = EncryptedNumber(np.poly1d(0))
            one = EncryptedNumber(np.poly1d(1))
            return result, zero, one

        whole_part = EncryptedNumber(enc_q)
        remains = EncryptedNumber(enc_r)

        return whole_part, remains, other
